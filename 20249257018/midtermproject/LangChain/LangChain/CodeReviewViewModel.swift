import Combine
import Foundation

@MainActor
final class CodeReviewViewModel: ObservableObject {
    @Published var sourceCode = ""
    @Published var review: ReviewResponse?
    @Published var logs: [DashboardLog] = []
    @Published var finalCode = ""
    @Published var healingSummary: [String] = []
    @Published var isAnalyzing = false
    @Published var isHealing = false
    @Published var analyzeStatus = "Ready for audit"
    @Published var healingStatus = "Waiting to run"
    @Published var errorMessage: String?

    private let client = APIClient()
    private var webSocketTask: URLSessionWebSocketTask?

    func analyze() async {
        isAnalyzing = true
        errorMessage = nil
        review = nil
        analyzeStatus = "Sending Swift code to the backend audit pipeline..."

        do {
            review = try await client.analyze(code: sourceCode)
            analyzeStatus = "Structured audit completed."
        } catch {
            errorMessage = error.localizedDescription
            analyzeStatus = "Audit failed."
        }

        isAnalyzing = false
    }

    func startSelfHealing() async {
        isHealing = true
        errorMessage = nil
        logs = []
        finalCode = ""
        healingSummary = []
        healingStatus = "Opening live self-healing stream..."

        do {
            try await streamSelfHealing()
        } catch {
            healingStatus = "Live stream failed. Switching to REST fallback..."
            logs.append(
                DashboardLog(
                    title: "Connection",
                    detail: "WebSocket stream failed, falling back to REST. \(error.localizedDescription)",
                    level: .failure
                )
            )

            do {
                let response = try await client.selfHeal(code: sourceCode, maxAttempts: 3)
                finalCode = response.finalCode
                healingSummary = response.summary
                healingStatus = response.success ? "REST fallback completed successfully." : "REST fallback completed with unresolved issues."
                logs.append(
                    DashboardLog(
                        title: "Summary",
                        detail: "Fallback completed with \(response.attempts.count) attempt(s). Success: \(response.success ? "yes" : "no")",
                        level: response.success ? .success : .failure
                    )
                )
                isHealing = false
            } catch {
                errorMessage = error.localizedDescription
                healingStatus = "Self-healing failed."
                isHealing = false
            }
        }
    }

    private func streamSelfHealing() async throws {
        let task = client.makeWebSocket()
        webSocketTask = task
        task.resume()
        healingStatus = "Connected. Waiting for agent reasoning..."

        let payload = try JSONEncoder().encode(SelfHealRequest(code: sourceCode, maxAttempts: 3))
        try await task.send(.string(String(decoding: payload, as: UTF8.self)))

        while true {
            let message = try await task.receive()
            guard case let .string(text) = message else { continue }
            let event = try JSONDecoder().decode(SelfHealingEvent.self, from: Data(text.utf8))
            consume(event: event)
            if event.type == "done" {
                isHealing = false
                task.cancel(with: .normalClosure, reason: nil)
                break
            }
        }
    }

    private func consume(event: SelfHealingEvent) {
        switch event.type {
        case "thought":
            healingStatus = event.message ?? "Agent is reasoning..."
            logs.append(DashboardLog(title: "Thought", detail: event.message ?? "", level: .info))
        case "observation":
            logs.append(
                DashboardLog(
                    title: "Build",
                    detail: event.message ?? "",
                    level: (event.succeeded ?? false) ? .success : .failure
                )
            )
            healingStatus = (event.succeeded ?? false) ? "Build succeeded." : "Build failed. Processing compiler feedback..."
            if let code = event.code {
                finalCode = code
            }
        case "done":
            finalCode = event.result?.finalCode ?? finalCode
            healingSummary = event.result?.summary ?? healingSummary
            healingStatus = event.result?.success == true ? "Workflow completed successfully." : "Workflow completed with unresolved issues."
            if let attempts = event.result?.attempts {
                logs.append(
                    DashboardLog(
                        title: "Summary",
                        detail: "Completed with \(attempts.count) attempt(s). Success: \(event.result?.success == true ? "yes" : "no")",
                        level: event.result?.success == true ? .success : .failure
                    )
                )
            }
        case "error":
            healingStatus = "Agent workflow failed."
            errorMessage = event.message
        default:
            break
        }
    }
}

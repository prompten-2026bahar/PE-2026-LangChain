import Foundation

struct APIClient {
    let baseURL: URL
    private let session: URLSession

    init(baseURL: URL = URL(string: "http://127.0.0.1:8000")!) {
        self.baseURL = baseURL
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 180
        configuration.timeoutIntervalForResource = 420
        self.session = URLSession(configuration: configuration)
    }

    func analyze(code: String) async throws -> ReviewResponse {
        var request = URLRequest(url: baseURL.appending(path: "analyze"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(AnalyzeRequest(code: code))

        let (data, response) = try await session.data(for: request)
        try validate(response: response, data: data)
        return try JSONDecoder().decode(ReviewResponse.self, from: data)
    }

    func selfHeal(code: String, maxAttempts: Int = 3) async throws -> SelfHealingResponse {
        var request = URLRequest(url: baseURL.appending(path: "self-heal"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(SelfHealRequest(code: code, maxAttempts: maxAttempts))

        let (data, response) = try await session.data(for: request)
        try validate(response: response, data: data)
        return try JSONDecoder().decode(SelfHealingResponse.self, from: data)
    }

    func makeWebSocket() -> URLSessionWebSocketTask {
        guard var components = URLComponents(url: baseURL, resolvingAgainstBaseURL: false) else {
            preconditionFailure("Invalid base URL")
        }
        components.scheme = baseURL.scheme == "https" ? "wss" : "ws"
        components.path = "/ws/self-heal"
        guard let wsURL = components.url else {
            preconditionFailure("Invalid WebSocket URL components")
        }
        return session.webSocketTask(with: wsURL)
    }

    private func validate(response: URLResponse, data: Data) throws {
        guard let httpResponse = response as? HTTPURLResponse, 200..<300 ~= httpResponse.statusCode else {
            let message = String(data: data, encoding: .utf8) ?? "Unknown API error"
            throw NSError(domain: "APIClient", code: 1, userInfo: [NSLocalizedDescriptionKey: message])
        }
    }
}

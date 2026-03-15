import Foundation

struct CodeIssue: Identifiable, Codable {
    let id = UUID()
    let line: Int
    let message: String
    let suggestion: String

    enum CodingKeys: String, CodingKey {
        case line
        case message
        case suggestion
    }
}

struct ReviewResponse: Codable {
    let score: Int
    let issues: [CodeIssue]
}

struct BuildAttempt: Identifiable, Codable {
    let id = UUID()
    let attempt: Int
    let thought: String
    let action: String
    let observation: String
    let code: String
    let succeeded: Bool

    enum CodingKeys: String, CodingKey {
        case attempt
        case thought
        case action
        case observation
        case code
        case succeeded
    }
}

struct SelfHealingResponse: Codable {
    let success: Bool
    let finalCode: String
    let attempts: [BuildAttempt]
    let summary: [String]

    enum CodingKeys: String, CodingKey {
        case success
        case finalCode = "final_code"
        case attempts
        case summary
    }
}

struct SelfHealingEvent: Codable {
    let type: String
    let attempt: Int?
    let message: String?
    let succeeded: Bool?
    let code: String?
    let result: SelfHealingResponse?
}

struct AnalyzeRequest: Codable {
    let code: String
}

struct SelfHealRequest: Codable {
    let code: String
    let maxAttempts: Int

    enum CodingKeys: String, CodingKey {
        case code
        case maxAttempts = "max_attempts"
    }
}

struct DashboardLog: Identifiable {
    let id = UUID()
    let title: String
    let detail: String
    let level: Level

    enum Level {
        case info
        case success
        case failure
    }
}

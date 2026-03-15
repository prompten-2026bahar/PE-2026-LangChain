import AppKit
import SwiftUI

private enum CodeTokenStyle {
    case plain
    case keyword
    case string
    case comment
    case number
    case type

    var color: Color {
        switch self {
        case .plain:
            return Color(red: 0.20, green: 0.24, blue: 0.31)
        case .keyword:
            return Color(red: 0.70, green: 0.16, blue: 0.40)
        case .string:
            return Color(red: 0.76, green: 0.39, blue: 0.11)
        case .comment:
            return Color(red: 0.44, green: 0.52, blue: 0.44)
        case .number:
            return Color(red: 0.23, green: 0.42, blue: 0.80)
        case .type:
            return Color(red: 0.11, green: 0.44, blue: 0.66)
        }
    }
}

private struct CodeToken: Identifiable {
    let id = UUID()
    let text: String
    let style: CodeTokenStyle
}

struct CodeBlockView: View {
    let title: String
    let code: String
    let placeholder: String
    @State private var didCopy = false
    private let titleColor = Color(red: 0.13, green: 0.16, blue: 0.22)
    private let chipTextColor = Color(red: 0.30, green: 0.35, blue: 0.44)
    private let chipBackground = Color(red: 0.88, green: 0.92, blue: 0.97)

    private let keywords: Set<String> = [
        "actor", "async", "await", "break", "case", "class", "continue", "default",
        "defer", "do", "else", "enum", "extension", "false", "for", "func", "guard",
        "if", "import", "in", "init", "let", "nil", "private", "protocol", "public",
        "return", "self", "static", "struct", "switch", "throw", "throws", "true",
        "try", "var", "where", "while"
    ]

    init(title: String, code: String, placeholder: String = "") {
        self.title = title
        self.code = code
        self.placeholder = placeholder
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(titleColor)
                Spacer()
                Button(didCopy ? "Copied" : "Copy") {
                    copyToClipboard()
                }
                .buttonStyle(.bordered)
                .controlSize(.small)
                .disabled(displayedCode.isEmpty)
                Text("Swift")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(chipTextColor)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(chipBackground, in: Capsule())
            }

            ScrollView {
                VStack(alignment: .leading, spacing: 0) {
                    ForEach(Array(displayedCode.lines.enumerated()), id: \.offset) { index, line in
                        HStack(alignment: .top, spacing: 12) {
                            Text("\(index + 1)")
                                .font(.system(size: 12, design: .monospaced))
                                .foregroundStyle(Color(red: 0.58, green: 0.61, blue: 0.68))
                                .frame(width: 34, alignment: .trailing)

                            highlightedLine(line)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 4)
                        .background(index.isMultiple(of: 2) ? Color.white.opacity(0.55) : Color.clear)
                    }
                }
                .padding(.vertical, 10)
            }
            .background(
                LinearGradient(
                    colors: [
                        Color(red: 0.96, green: 0.97, blue: 0.99),
                        Color(red: 0.92, green: 0.95, blue: 0.98)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                ),
                in: RoundedRectangle(cornerRadius: 18, style: .continuous)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 18, style: .continuous)
                    .stroke(Color(red: 0.82, green: 0.86, blue: 0.91), lineWidth: 1)
            )
        }
    }

    private func highlightedLine(_ line: String) -> Text {
        if line.isEmpty {
            return Text(" ")
                .font(.system(size: 13, design: .monospaced))
        }

        return tokens(for: line).reduce(Text("")) { partial, token in
            partial + Text(token.text)
                .foregroundStyle(token.style.color)
                .font(.system(size: 13, design: .monospaced))
        }
    }

    private var displayedCode: String {
        code.isEmpty ? placeholder : code
    }

    private func copyToClipboard() {
        let text = displayedCode
        guard !text.isEmpty else { return }
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(text, forType: .string)
        didCopy = true

        Task {
            try? await Task.sleep(for: .seconds(1.2))
            await MainActor.run {
                didCopy = false
            }
        }
    }

    private func tokens(for line: String) -> [CodeToken] {
        var tokens: [CodeToken] = []
        var current = ""
        var index = line.startIndex

        while index < line.endIndex {
            let character = line[index]
            let nextIndex = line.index(after: index)

            if character == "/" && nextIndex < line.endIndex && line[nextIndex] == "/" {
                flushCurrent(&current, into: &tokens)
                tokens.append(CodeToken(text: String(line[index...]), style: .comment))
                break
            }

            if character == "\"" {
                flushCurrent(&current, into: &tokens)
                var stringEnd = nextIndex
                var escaped = false
                while stringEnd < line.endIndex {
                    let char = line[stringEnd]
                    if char == "\"" && !escaped {
                        stringEnd = line.index(after: stringEnd)
                        break
                    }
                    escaped = char == "\\" && !escaped
                    if char != "\\" {
                        escaped = false
                    }
                    stringEnd = line.index(after: stringEnd)
                }
                tokens.append(CodeToken(text: String(line[index..<stringEnd]), style: .string))
                index = stringEnd
                continue
            }

            if character.isWholeNumber {
                flushCurrent(&current, into: &tokens)
                var numberEnd = nextIndex
                while numberEnd < line.endIndex && line[numberEnd].isWholeNumber {
                    numberEnd = line.index(after: numberEnd)
                }
                tokens.append(CodeToken(text: String(line[index..<numberEnd]), style: .number))
                index = numberEnd
                continue
            }

            if character.isLetter || character == "_" {
                current.append(character)
                index = nextIndex
                while index < line.endIndex && (line[index].isLetter || line[index].isNumber || line[index] == "_") {
                    current.append(line[index])
                    index = line.index(after: index)
                }
                appendIdentifier(current, into: &tokens)
                current.removeAll(keepingCapacity: true)
                continue
            }

            flushCurrent(&current, into: &tokens)
            tokens.append(CodeToken(text: String(character), style: .plain))
            index = nextIndex
        }

        flushCurrent(&current, into: &tokens)
        return tokens
    }

    private func appendIdentifier(_ identifier: String, into tokens: inout [CodeToken]) {
        if keywords.contains(identifier) {
            tokens.append(CodeToken(text: identifier, style: .keyword))
        } else if identifier.first?.isUppercase == true {
            tokens.append(CodeToken(text: identifier, style: .type))
        } else {
            tokens.append(CodeToken(text: identifier, style: .plain))
        }
    }

    private func flushCurrent(_ current: inout String, into tokens: inout [CodeToken]) {
        guard !current.isEmpty else { return }
        tokens.append(CodeToken(text: current, style: .plain))
        current.removeAll(keepingCapacity: true)
    }
}

private extension String {
    var lines: [String] {
        let splitLines = self.split(separator: "\n", omittingEmptySubsequences: false).map(String.init)
        return splitLines.isEmpty ? [""] : splitLines
    }
}

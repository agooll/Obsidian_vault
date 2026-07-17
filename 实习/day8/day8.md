### write_to_file 中文引号转换问题
开发
- **问题**：`write_to_file` 工具会将 Unicode 中文左右双引号 `\u201c`（"）和 `\u201d`（"）转换为 ASCII 直双引号 `\u0022`（"）
- **影响**：当 JSON 字符串值中包含中文引号时（如 `"打开"抖音"应用"`），转换后变成 `"打开"抖音"应用"`，导致 JSON 解析失败（`JSONDecodeError`）
- **解决方案**：对于包含中文引号的 JSON 输出，必须使用 Python `json.dump()` 写入文件，而非 `write_to_file` 工具
- **触发条件**：`optimization_result.json` 中步骤内容的 UI 文案需要用中文双引号（符合 base-spec 规范），且通过 `write_to_file` 写入时

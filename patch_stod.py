import os
import re

filepath = "src/services.cpp"
with open(filepath, "r") as f:
    content = f.read()

safe_stod_code = """
#include <iostream>
#include <stdexcept>

static double safeStod(const std::string& str, double defaultVal = 0.0) {
    if (str.empty()) return defaultVal;
    try {
        return std::stod(str);
    } catch (const std::out_of_range&) {
        std::cerr << "[DATA ERROR] std::out_of_range parsing double from: " << str << "\\n";
        if (str.find("e-") != std::string::npos || str.find("E-") != std::string::npos) {
            return 0.0; // handle underflow gracefully
        }
        return defaultVal;
    } catch (const std::invalid_argument&) {
        std::cerr << "[DATA ERROR] std::invalid_argument parsing double from: " << str << "\\n";
        return defaultVal;
    } catch (...) {
        std::cerr << "[DATA ERROR] Unknown error parsing double from: " << str << "\\n";
        return defaultVal;
    }
}
"""

if "safeStod(" not in content:
    # Insert it after the includes
    # Find the last include
    last_include = 0
    for i, line in enumerate(content.split('\\n')):
        if line.startswith("#include"):
            last_include = i
    
    lines = content.split('\\n')
    lines.insert(last_include + 1, safe_stod_code)
    content = "\\n".join(lines)

# Replace all std::stod with safeStod
content = content.replace("std::stod", "safeStod")

with open(filepath, "w") as f:
    f.write(content)
print("services.cpp patched successfully!")

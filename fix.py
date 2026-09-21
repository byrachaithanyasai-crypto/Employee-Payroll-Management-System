import os
import re

with open("src/services.cpp", "r") as f:
    text = f.read()

# Replace the broken block
broken = """out << "\\n
#include <iostream>
#include <stdexcept>

static double safeStod(const std::string& str, double defaultVal = 0.0) {
    if (str.empty()) return defaultVal;
    try {
        return safeStod(str);
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
\\n";"""

if broken in text:
    text = text.replace(broken, 'out << "\\n";')

# Replace safeStod with safeParseDouble
text = text.replace('safeStod', 'safeParseDouble')
text = text.replace('std::stod', 'safeParseDouble')

safe_parse_func = """
#include <iostream>
#include <stdexcept>

inline double safeParseDouble(const std::string& str, double defaultVal = 0.0) {
    if (str.empty()) return defaultVal;
    try {
        return std::stod(str);
    } catch (const std::out_of_range&) {
        std::cerr << "\\n[DATA ERROR] std::out_of_range parsing double from: " << str << "\\n";
        if (str.find("e-") != std::string::npos || str.find("E-") != std::string::npos) {
            return 0.0; 
        }
        return defaultVal;
    } catch (const std::invalid_argument&) {
        std::cerr << "\\n[DATA ERROR] std::invalid_argument parsing double from: " << str << "\\n";
        return defaultVal;
    } catch (...) {
        std::cerr << "\\n[DATA ERROR] Unknown error parsing double from: " << str << "\\n";
        return defaultVal;
    }
}
"""

if "safeParseDouble(const std::string& str" not in text:
    # Insert it right after the includes
    match = re.search(r'#include <iostream>', text)
    if match:
        text = text[:match.end()] + "\\n" + safe_parse_func + text[match.end():]

with open("src/services.cpp", "w") as f:
    f.write(text)

print("Fixed services.cpp!")

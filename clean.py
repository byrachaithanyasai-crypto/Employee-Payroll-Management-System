import os
import re

filepath = "src/services.cpp"
with open(filepath, "r") as f:
    content = f.read()

# Let's remove the bad safeStod definition block that was inserted
start = content.find('#include <iostream>')
end = content.find('static double safeStod(const std::string& str, double defaultVal = 0.0) {')
# Actually, the bad one is exactly what I output earlier. Let's just find the exact block and remove it.
bad_block = """
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
\\n";
"""
content = content.replace(bad_block, "")
content = content.replace("safeStod", "std::stod")

# Now insert safeStod safely at the top
safe_stod_code = """
#include <iostream>
#include <stdexcept>

inline double safeStod(const std::string& str, double defaultVal = 0.0) {
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

lines = content.split('\\n')
# remove the line that has "\n"; which caused the syntax error
lines = [l for l in lines if l.strip() != '\\n";' and l.strip() != 'return safeStod(str);']

# Let's write a clean fresh replacement logic:
def clean_file():
    with open("src/services.cpp", "r") as f:
        text = f.read()
    
    # We will look for std::stod and replace it with safeStod
    # We will also insert safeStod just after #include <iostream>
    # If the file is messy, let's just wipe out safeStod completely and try again.
    
    # Find the top of the file
    text = re.sub(r'static double safeStod.*?(?=\\n\\n)', '', text, flags=re.DOTALL)
    # Revert all safeStod to std::stod
    text = text.replace('safeStod', 'std::stod')
    
    # Let's fix the broken audit.log string
    text = text.replace('out << "\\n', 'out << "\\n";\\n')
    
    # Insert safeStod
    import re
    match = re.search(r'#include <iostream>', text)
    if match:
        idx = match.end()
        text = text[:idx] + "\\n" + safe_stod_code + text[idx:]
        
    text = text.replace('std::stod', 'safeStod')
    text = text.replace('inline double safeStod', 'inline double std::stod') # revert the declaration to not be replaced
    text = text.replace('return safeStod(str);', 'return std::stod(str);') # revert the inside
    
    with open("src/services.cpp", "w") as f:
        f.write(text)

clean_file()
print("Cleaned!")

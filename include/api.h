#pragma once
#include <map>
#include <string>
#include "models.h"

void startApiServer(int port, std::map<std::string, User>& appUsers);

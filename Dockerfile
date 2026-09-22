FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN chmod +x BUILD.bat RUN_SERVER.bat 2>/dev/null || true

RUN g++ -std=c++17 -O2 -Iinclude \
    -o payroll_backend src/*.cpp

EXPOSE 8080

CMD ["./payroll_backend"]
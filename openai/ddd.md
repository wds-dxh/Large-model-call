# MPU6050 类说明文档

## 概述

`MPU6050` 类提供了一个封装的接口来与 MPU6050 传感器进行交互，允许用户获取加速度和陀螺仪数据。该类隐藏了复杂的初始化和数据采集细节，提供了简单易用的 API。

## 功能

- **构造函数**：初始化 MPU6050 传感器，设置量程和滤波器。
- **析构函数**：清理资源，结束 I2C 通信。
- **get_data**：获取传感器的当前数据。

## 各个函数的介绍

### 构造函数

```cpp
MPU6050::MPU6050(uint8_t scl, uint8_t sda)
```

- **简介**：初始化 MPU6050 传感器，设置量程和滤波器。
- **参数**：
  - `scl`：I2C 总线的时钟线引脚。
  - `sda`：I2C 总线的数据信号线引脚。
- **说明**：构造函数使用提供的 `scl` 和 `sda` 引脚初始化 I2C 总线，并检查 MPU6050 芯片是否正确连接。如果芯片未找到，程序将停止执行。成功连接后，设置加速度计和陀螺仪的量程，以及滤波器的带宽。

### 析构函数

```cpp
MPU6050::~MPU6050()
```

- **简介**：清理 MPU6050 实例使用的资源。
- **说明**：析构函数结束 I2C 通信，并释放与 `mpu` 对象相关的内存。

### 获取数据

```cpp
MPU6050::mpu6050_data MPU6050::get_data()
```

- **简介**：从 MPU6050 传感器获取当前的温度、加速度和陀螺仪数据。
- **说明**：该函数读取传感器数据，填充一个 `mpu6050_data` 结构体，并返回。结构体中包含温度（摄氏度）、加速度（X、Y、Z 轴，单位为 g），以及陀螺仪（X、Y、Z 轴，单位为 deg/s）的数据。

## 示例代码

```cpp
#include "MPU6050_HPP"

void setup() {
    Serial.begin(115200);
    MPU6050 mpu6050(21, 22); // 使用 ESP32 的 GPIO 21 (SCL) 和 GPIO 22 (SDA)
    Serial.println("MPU6050 initialized");
}

void loop() {
    MPU6050::mpu6050_data data = mpu6050.get_data(); // 获取数据
    Serial.print("Temperature: ");
    Serial.print(data.temperature);
    Serial.println(" C");
    Serial.print("Acc X: ");
    Serial.print(data.accX);
    Serial.print(" Y: ");
    Serial.print(data.accY);
    Serial.print(" Z: ");
    Serial.println(data.accZ);
    Serial.print("Gyro X: ");
    Serial.print(data.gyroX);
    Serial.print(" Y: ");
    Serial.print(data.gyroY);
    Serial.print(" Z: ");
    Serial.println(data.gyroZ);
    delay(100); // 稍作延迟，避免过快刷新
}
```

## 注意事项

1. **I2C 引脚选择**：确保选择的 I2C 引脚与您的硬件连接相匹配。
2. **电源稳定性**：确保 MPU6050 传感器接收到稳定的电源供应。
3. **错误处理**：如果传感器未正确连接或初始化失败，程序将停止执行。请检查您的硬件连接。
4. **数据更新频率**：获取数据的频率不应过高，以免影响传感器的稳定性和电池寿命（如果使用电池供电）。

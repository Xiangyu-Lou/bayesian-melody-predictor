import numpy as np
from scipy.optimize import minimize
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

# 模拟数据和训练GP模型
# 假设训练数据是 1D 的
X_train = np.random.rand(50, 1)  # 1D 输入
y_train = 2 * X_train[:, 0] + np.sin(5 * X_train[:, 0])  # 非线性目标函数

# 训练 GP 模型
kernel = RBF(length_scale=1.0)
gp_model = GaussianProcessRegressor(kernel=kernel, alpha=1e-6)
gp_model.fit(X_train, y_train)

# 定义目标输出值
target_y = 1.5  # 目标值

# 定义目标函数：最小化预测值与目标值之间的偏差
def objective(x):
    y_pred, _ = gp_model.predict(x.reshape(1, -1))  # GP模型预测值
    return np.abs(y_pred - target_y)  # 与目标值的绝对偏差

# 初始输入点，随机初始化（1D 输入时）
x0 = np.random.rand(1, 1)  # 可调整为更高维度输入

# 优化找到最接近目标输出的输入
res = minimize(objective, x0=x0, bounds=[(0, 1)])  # 输入范围设为 [0, 1]

# 获取最优输入点
optimal_x = res.x

# 在最优点上查询预测方差
y_pred, variance = gp_model.predict(optimal_x.reshape(1, -1), return_std=True)
variance = variance**2  # 方差 = 标准差的平方

# 打印结果
print(f"目标输出值: {target_y}")
print(f"最优输入点: {optimal_x}")
print(f"模型预测的值: {y_pred[0]}")
print(f"对应的预测方差: {variance[0]}")

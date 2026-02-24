import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建图形
fig = plt.figure(figsize=(14, 6))

# ====== 左侧：正方形上的点 ======
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_aspect('equal')
ax1.set_xlim(-0.5, 12.5)
ax1.set_ylim(-0.5, 7.5)
ax1.set_title('Square: 12 Points on y=(7/12)x')

# 画正方形
square_x = [0, 12, 12, 0, 0]
square_y = [0, 0, 7, 7, 0]
ax1.plot(square_x, square_y, 'k-', linewidth=2, alpha=0.7)

# 画线 y = (7/12)x
x_line = np.linspace(0, 12, 100)
y_line = (7/12) * x_line
ax1.plot(x_line, y_line, 'b-', linewidth=2, alpha=0.7)

# 12个点
x_points = list(range(12))
y_points = [(7/12) * x for x in x_points]

note_names = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
colors = ['#FF0000', '#FF6600', '#FFCC00', '#99FF00', '#00FF66',
          '#00FFFF', '#0066FF', '#6600FF', '#CC00FF', '#FF0099',
          '#FF0066', '#FF3333']

for i, (x, y) in enumerate(zip(x_points, y_points)):
    ax1.plot(x, y, 'o', color=colors[i], markersize=10, 
             markeredgecolor='black', markeredgewidth=1.5)
    ax1.text(x + 0.4, y + 0.25, note_names[i], fontsize=10, fontweight='bold')

ax1.set_xlabel('x (fifths)')
ax1.set_ylabel('y (octaves)')
ax1.grid(True, alpha=0.2)

# ====== 右侧：修正 - 点在扭结上 ======
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.set_title('Torus: 12 Points on T(7,12) KNOT (Corrected)\n(Drag to rotate)')

# 环面参数
R, r = 2.5, 0.8
p, q = 7, 12

# 生成扭结 T(7,12)
t_full = np.linspace(0, 2*np.pi, 1000)
X_knot = (R + r*np.cos(p*t_full)) * np.cos(q*t_full)
Y_knot = (R + r*np.cos(p*t_full)) * np.sin(q*t_full)
Z_knot = r * np.sin(p*t_full)

# 画完整的扭结
ax2.plot(X_knot, Y_knot, Z_knot, 'b-', linewidth=2, alpha=0.6)

# 非常淡的环面背景（几乎看不见）
u = np.linspace(0, 2*np.pi, 25)
v = np.linspace(0, 2*np.pi, 15)
U, V = np.meshgrid(u, v)
X_torus = (R + r*np.cos(V)) * np.cos(U)
Y_torus = (R + r*np.cos(V)) * np.sin(U)
Z_torus = r * np.sin(V)
ax2.plot_wireframe(X_torus, Y_torus, Z_torus, alpha=0.05, color='gray', linewidth=0.2)

# 关键修正：计算点在扭结上的位置（不是环面表面！）
# 对于正方形上的点(x,y)，对应的参数t满足：
# x/12 = t/(2π) 的 q 分量？不对...
# 实际上：在正方形上，点参数是 t = 2π * x/12
# 但在扭结上，我们需要找到正确的 t 值使得点在扭结上

# 正确方法：扭结参数方程中的 t 对应正方形上的某种线性关系
# 扭结：θ = q*t, φ = p*t （θ是经度，φ是纬度）
# 正方形：x 对应 θ，y 对应 φ
# 所以：θ = 2π*x/12, φ = 2π*y/7
# 因此：q*t = 2π*x/12, p*t = 2π*y/7
# 由于 y = (7/12)x，所以 p*t = 2π*(7/12)x/7 = 2π*x/12
# 所以 q*t = p*t ⇒ 除非 t=0，否则不可能... 这里有问题

# 等等，我搞混了。让我们重新思考：
# 在正方形上，我们有点 (x, (7/12)x)
# 映射到环面：θ = 2π*x/12, φ = 2π*(7/12)x/7 = 2π*x/12
# 所以 θ = φ！这意味着点在环面的对角线上

# 但扭结 T(7,12) 是：θ = q*t, φ = p*t = 7t
# 所以如果 θ = φ，那么 q*t = p*t ⇒ (q-p)t = 0 ⇒ t=0
# 这说明只有起点在扭结上？

# 啊！我明白了错误所在：
# 正方形上的直线 y=(7/12)x 映射到环面上是：θ=2π*x/12, φ=2π*x/12
# 这是环面的对角线（θ=φ），不是扭结 T(7,12)！
# 扭结 T(7,12) 是：θ=12t, φ=7t

# 所以我们需要找的是：对于哪些t，点(12t/(2π), 7t/(2π))在正方形直线上？
# 即：7t/(2π) = (7/12) * (12t/(2π)) = 7t/(2π) ← 恒成立！
# 所以整条扭结都对应正方形上的直线！

# 那么正方形上的点 x=0..11 对应 t = 2π*x/12
print("\n计算点在扭结上的参数 t:")
t_values = []
for x in x_points:
    t = 2 * np.pi * x / 12  # 因为 θ = q*t = 12t，而 θ = 2π*x/12
    t_values.append(t)
    print(f"x={x:2d} ({note_names[x]}): t = {t:.3f}")

# 现在用这些 t 值计算扭结上的点
for i, t in enumerate(t_values):
    x_torus = (R + r*np.cos(p*t)) * np.cos(q*t)
    y_torus = (R + r*np.cos(p*t)) * np.sin(q*t)
    z_torus = r * np.sin(p*t)
    
    # 画点（在扭结上！）
    ax2.plot([x_torus], [y_torus], [z_torus], 'o', 
             color=colors[i], markersize=12,
             markeredgecolor='black', markeredgewidth=2, alpha=1.0)
    
    # 添加标签
    offset = 0.3
    ax2.text(x_torus+offset, y_torus+offset, z_torus+offset, 
             note_names[i], fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))

# 标记起点C特别突出
t0 = t_values[0]
x0 = (R + r*np.cos(p*t0)) * np.cos(q*t0)
y0 = (R + r*np.cos(p*t0)) * np.sin(q*t0)
z0 = r * np.sin(p*t0)
ax2.plot([x0], [y0], [z0], '*', 
         color='lime', markersize=22, markeredgecolor='black', 
         markeredgewidth=2, alpha=1.0)

# 验证：这些点应该在扭结上
# 让我们采样一些中间点验证
print("\n验证点是否在扭结上（取几个样本）:")
sample_indices = [0, 3, 6, 9]
for idx in sample_indices:
    t = t_values[idx]
    # 从参数方程计算
    x_calc = (R + r*np.cos(p*t)) * np.cos(q*t)
    y_calc = (R + r*np.cos(p*t)) * np.sin(q*t)
    z_calc = r * np.sin(p*t)
    print(f"{note_names[idx]}: t={t:.3f}, pos=({x_calc:.3f}, {y_calc:.3f}, {z_calc:.3f})")

# 设置视角
ax2.view_init(elev=25, azim=45)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

# 移除刻度
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_zticks([])

# 范围
margin = 0.5
ax2.set_xlim(-R-r-margin, R+r+margin)
ax2.set_ylim(-R-r-margin, R+r+margin)
ax2.set_zlim(-r-margin, r+margin)

ax2.text2D(0.02, 0.98, '← Points ON the knot\n   Not on torus surface', 
           transform=ax2.transAxes, fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("关键理解：")
print("="*60)
print("1. 正方形上的直线 y=(7/12)x 对应环面的一条曲线")
print("2. 这条曲线恰好是 T(7,12) 环面扭结")
print("3. 正方形上的点 x=0..11 映射到扭结上的点")
print("4. 映射公式：t = 2π * x / 12")
print("5. 然后代入扭结参数方程：")
print("   X = (R + r·cos(7t))·cos(12t)")
print("   Y = (R + r·cos(7t))·sin(12t)")
print("   Z = r·sin(7t)")
print("6. 现在所有彩色点都在蓝色扭结曲线上！")
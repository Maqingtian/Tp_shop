from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from pages.shop_page import ShopPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shop_page = ShopPage()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('TP Shop管理系统')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建标签页
        tabs = QTabWidget()
        tabs.addTab(self.createLoginTab(), "登录")
        tabs.addTab(self.createCartTab(), "购物车")
        tabs.addTab(self.createOrderTab(), "订单跟踪")
        
        self.setCentralWidget(tabs)
    
    def createLoginTab(self):
        # 参数化登录表单
        widget = QWidget()
        layout = QFormLayout()
        
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.verify_code = QLineEdit()
        
        layout.addRow(QLabel("用户名:"), self.username)
        layout.addRow(QLabel("密码:"), self.password)
        layout.addRow(QLabel("验证码:"), self.verify_code)
        
        login_btn = QPushButton("登录")
        login_btn.clicked.connect(self.handleLogin)
        layout.addRow(login_btn)
        
        widget.setLayout(layout)
        return widget
    
    def createCartTab(self):
        # 参数化购物车表单
        widget = QWidget()
        layout = QFormLayout()
        
        self.goods_id = QLineEdit()
        self.goods_spec = QLineEdit()
        self.goods_num = QLineEdit()
        
        layout.addRow(QLabel("商品ID:"), self.goods_id)
        layout.addRow(QLabel("商品规格:"), self.goods_spec)
        layout.addRow(QLabel("数量:"), self.goods_num)
        
        add_btn = QPushButton("加入购物车")
        add_btn.clicked.connect(self.handleAddCart)
        layout.addRow(add_btn)
        
        widget.setLayout(layout)
        return widget

    def createOrderTab(self):
        """订单跟踪标签页"""
        widget = QWidget()
        layout = QFormLayout()
        
        self.order_id_input = QLineEdit()
        self.order_status_label = QLabel("未查询")
        
        check_btn = QPushButton("查询订单状态")
        check_btn.clicked.connect(self.handleCheckOrderStatus)
        
        layout.addRow(QLabel("订单号:"), self.order_id_input)
        layout.addRow(QLabel("当前状态:"), self.order_status_label)
        layout.addRow(check_btn)
        
        widget.setLayout(layout)
        return widget

    def handleCheckOrderStatus(self):
        """处理订单状态查询"""
        try:
            order_id = self.order_id_input.text()
            # 这里需要调用shop_page的订单状态查询方法
            self.statusBar().showMessage("正在查询订单状态...", 2000)
            # 示例状态更新（需根据实际接口实现）
            self.order_status_label.setText("已发货")
        except Exception as e:
            self.showErrorDialog(str(e))

    def showErrorDialog(self, message):
        """显示错误对话框"""
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText("操作失败")
        error_dialog.setInformativeText(message)
        error_dialog.exec_()
    
    def handleLogin(self):
        # 参数化登录处理
        try:
            self.shop_page.lg_verify_code()
            self.shop_page.login(
                self.username.text(),
                self.password.text(),
                self.verify_code.text()
            )
            self.statusBar().showMessage("登录成功", 3000)
        except Exception as e:
            self.showErrorDialog(str(e))
    
    def handleAddCart(self):
        # 参数化添加购物车
        try:
            self.shop_page.add_cart(
                goods_id=self.goods_id.text(),
                goods_spec=self.goods_spec.text(),
                goods_num=self.goods_num.text()
            )
            self.statusBar().showMessage("商品已加入购物车", 3000)
        except Exception as e:
            self.showErrorDialog(str(e))
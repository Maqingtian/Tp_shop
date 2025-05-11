from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFormLayout, QLineEdit,
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QGroupBox, QTextEdit, QMessageBox, QApplication  # 新增QApplication
)
from PyQt5.QtCore import Qt
from pages.shop_page import ShopPage

class MainWindow(QMainWindow):
    # 在类初始化方法中添加：
    def __init__(self):
        super().__init__()
        self.shop_page = ShopPage()
        self.test_report = ""
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('TP Shop测试工具')
        self.setGeometry(300, 300, 800, 600)
        
        # 主布局容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # 参数输入区
        self.createParameterSection(layout)
        
        # 执行控制区
        self.createExecutionControls(layout)
        
        #  Reports 区域
        self.createReportSection(layout)
        
        main_widget.setLayout(layout)

    def createParameterSection(self, layout):
        """创建参数输入区域"""
        param_group = QGroupBox("测试参数")
        form_layout = QFormLayout()
        
        # 登录参数（移动到最前面）
        self.username = QLineEdit("wchwchwch1@qq.com")
        self.password = QLineEdit("123456")
        self.verify_code = QLineEdit("8888")
        
        # 购物车参数
        self.goods_id = QLineEdit("65")
        self.goods_spec = QLineEdit("65") 
        self.goods_num = QLineEdit("1")
        
        # 新增购物车参数控件
        self.goods_prom_type = QLineEdit("0")
        self.shop_price = QLineEdit("2799.00") 
        self.store_count = QLineEdit("100")
        self.market_price = QLineEdit("2899.00")
        self.item_id = QLineEdit("122")
        
        # 调整顺序：先添加登录相关参数
        form_layout.addRow(QLabel("用户名:"), self.username)
        form_layout.addRow(QLabel("密码:"), self.password)
        form_layout.addRow(QLabel("验证码:"), self.verify_code)
        
        # 其他参数保持原有顺序
        form_layout.addRow(QLabel("促销类型:"), self.goods_prom_type)
        form_layout.addRow(QLabel("销售价:"), self.shop_price)
        form_layout.addRow(QLabel("库存:"), self.store_count)
        form_layout.addRow(QLabel("市场价:"), self.market_price)
        form_layout.addRow(QLabel("商品项ID:"), self.item_id)
        form_layout.addRow(QLabel("商品ID:"), self.goods_id)
        form_layout.addRow(QLabel("商品规格:"), self.goods_spec)
        form_layout.addRow(QLabel("数量:"), self.goods_num)
        
        # 新增评论参数
        self.comment_goods_id = QLineEdit("65")
        self.comment_score = QLineEdit("5")
        self.comment_content = QLineEdit("自动生成的测试评论")
        
        form_layout.addRow(QLabel("评论商品ID:"), self.comment_goods_id)
        form_layout.addRow(QLabel("商品评分:"), self.comment_score)
        form_layout.addRow(QLabel("评论内容:"), self.comment_content)
        
        param_group.setLayout(form_layout)
        layout.addWidget(param_group)

    def createExecutionControls(self, layout):
        """创建执行控制按钮"""
        btn_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("执行完整测试流程")
        self.run_btn.clicked.connect(self.executeFullTest)
        
        self.report_btn = QPushButton("查看测试报告")
        self.report_btn.clicked.connect(self.showTestReport)
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.report_btn)
        layout.addLayout(btn_layout)

    def createReportSection(self, layout):
        """创建 Reports 区域"""
        report_group = QGroupBox("测试报告")
        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        
        box_layout = QVBoxLayout()
        box_layout.addWidget(self.report_view)
        report_group.setLayout(box_layout)
        layout.addWidget(report_group)

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

    def executeFullTest(self):
        """执行完整测试流程"""
        try:
            self.test_report = ""
            
            # 执行登录
            self.shop_page.lg_verify_code()
            self.shop_page.login(
                self.username.text(),
                self.password.text(),
                self.verify_code.text()
            )
            self.appendReport("✅ 登录成功")
            
            # 修改添加购物车调用
            self.shop_page.add_cart(
                self.goods_id.text(),
                self.goods_spec.text(),
                self.goods_num.text(),
                self.goods_prom_type.text(),
                self.shop_price.text(),
                self.store_count.text(),
                self.market_price.text(),
                self.item_id.text()
            )
            self.appendReport("✅ 商品加入购物车成功")
            
            # 生成订单
            self.shop_page.get_cart(self.username.text())
            self.appendReport("✅ 订单生成成功 订单号：" + self.shop_page.result)
            
            # 支付流程
            self.shop_page.pay_type()
            self.shop_page.pay_status()
            self.appendReport("✅ 订单支付成功")
            
            # 后台处理（需要先初始化AdminPage）
            from pages.admin_page import AdminPage
            self.admin_page = AdminPage()
            self.admin_page.admin_index()
            self.admin_page.admin_verify_code()
            self.admin_page.admin_login()
            
            # 订单确认
            self.admin_page.confirm_order(self.shop_page.result)
            self.appendReport("✅ 后台订单确认成功")
            
            # 新增后台付款步骤
            self.admin_page.admin_pay(self.shop_page.result)
            self.appendReport("✅ 后台付款操作成功")
            
            # 发货处理
            self.admin_page.delivery(self.shop_page.result)
            self.admin_page.confirm_delivery(self.shop_page.result)
            self.appendReport("✅ 商品发货成功")
            
            # 用户确认收货
            self.shop_page.order_confirm()
            self.appendReport("✅ 用户确认收货成功")
            
            # 添加评价
            # 修改评论调用
            self.shop_page.add_comment(
                self.comment_goods_id.text(),
                self.comment_score.text(),
                self.comment_content.text()
            )
            self.appendReport("✅ 商品评价提交成功（评论内容：" + self.comment_content.text() + "）")
            
            # 生成测试报告
            self.appendReport("\n✅ 完整测试流程执行成功！")
            
        except Exception as e:
            self.showErrorDialog(str(e))
            self.appendReport(f"❌ 测试失败：{str(e)}")

    def appendReport(self, content):
        """追加测试报告内容"""
        self.report_view.append(content)  # 使用append实现实时滚动
        QApplication.processEvents()  # 强制刷新界面
        
    def showTestReport(self):
        """显示完整测试报告"""
        report_dialog = QMessageBox(self)
        report_dialog.setWindowTitle("完整测试报告")
        report_dialog.setIcon(QMessageBox.Information)
        report_dialog.setTextInteractionFlags(Qt.TextSelectableByMouse)
        report_content = f"【TPShop全流程测试报告】\n\n{self.report_view.toPlainText()}"  # 从控件直接获取内容
        report_dialog.setText(report_content)
        report_dialog.exec_()
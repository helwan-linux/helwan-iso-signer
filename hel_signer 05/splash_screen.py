from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QEventLoop, QTimer

def show_splash(app, duration=3000):
    """
    Displays the Helwan ISO Signer splash screen and keeps it visible
    for the full duration (in milliseconds).
    """
    # مساحة الرسم
    pixmap = QPixmap(420, 260)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # الخلفية
    painter.setBrush(QColor("#0e2626"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, 420, 260, 18, 18)

    # النص
    painter.setPen(QColor("#2ec4b6"))
    font = QFont("Ubuntu", 16, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Helwan ISO Signer\nLoading components...")

    painter.end()

    # إنشاء وعرض شاشة الترحيب
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    splash.show()

    # نضمن بقاءها ظاهرة فعلاً المدة المطلوبة
    loop = QEventLoop()
    QTimer.singleShot(duration, loop.quit)
    loop.exec_()  # يمنع البرنامج من الاستمرار إلا بعد المدة المحددة

    return splash

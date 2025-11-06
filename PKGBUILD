pkgname=hel-iso-signer
_pkgname=helwan-iso-signer
pkgver=1
pkgrel=0.1
pkgdesc="أداة رسومية احترافية لتوقيع ملفات ISO وتوليد بيانات الإصدار (SHA/GPG)."
arch=('any')
url="https://github.com/helwan-linux/helwan-iso-signer"
license=('GPL3')
depends=('python' 'python-pyqt5' 'gnupg')
makedepends=('git')

# المصدر: Git repo
source=("git+https://github.com/helwan-linux/helwan-iso-signer.git")
sha256sums=('SKIP')


package() {
    _app_dir="/usr/lib/${pkgname}"
    _git_src_dir="${srcdir}/${_pkgname}"

    mkdir -p "${pkgdir}/${_app_dir}"

    # نسخ ملفات Python والموارد
    install -m 644 "${_git_src_dir}/signer_gui.py" "${pkgdir}/${_app_dir}/"
    install -m 644 "${_git_src_dir}/signer_logic.py" "${pkgdir}/${_app_dir}/"
    install -m 644 "${_git_src_dir}/splash_screen.py" "${pkgdir}/${_app_dir}/"
    install -m 644 "${_git_src_dir}/helwan_style.qss" "${pkgdir}/${_app_dir}/"

    # نسخ الأيقونة
    install -Dm644 "${_git_src_dir}/signer_icon.png" "${pkgdir}/${_app_dir}/signer_icon.png"
    install -Dm644 "${_git_src_dir}/signer_icon.png" "${pkgdir}/usr/share/icons/hicolor/128x128/apps/${_pkgname}.png"

    # ملف التشغيل في /usr/bin
    mkdir -p "${pkgdir}/usr/bin/"
    cat > "${pkgdir}/usr/bin/${_pkgname}" << EOT
#!/bin/bash
python3 -B /usr/lib/${_pkgname}/signer_gui.py "\$@"
EOT
    chmod 755 "${pkgdir}/usr/bin/${_pkgname}"

    # ملف Desktop Entry
    mkdir -p "${pkgdir}/usr/share/applications/"
    cat > "${pkgdir}/usr/share/applications/${_pkgname}.desktop" << EOT
[Desktop Entry]
Name=Helwan ISO Signer
Comment=A professional GUI tool for signing ISO files and generating release data (SHA/GPG).
Exec=${_pkgname}
Icon=${_pkgname}
Terminal=false
Type=Application
Categories=Utility;Security;Development;
StartupNotify=true
EOT
}

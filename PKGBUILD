pkgname=helwan-iso-signer
pkgver=1.0
pkgrel=1
pkgdesc="A professional GUI tool for signing ISO files and generating release data (SHA/GPG)"
arch=('any')
url="https://github.com/helwan-linux/helwan-iso-signer"
license=('MIT')
depends=('python' 'python-pyqt5' 'gnupg')
source=("$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm755 signer_gui.py "$pkgdir/usr/bin/helwan-signer"
    install -Dm644 signer_icon.png "$pkgdir/usr/share/icons/hicolor/256x256/apps/helwan-iso-signer.png"
    install -Dm644 helwan-iso-signer.desktop "$pkgdir/usr/share/applications/helwan-iso-signer.desktop"
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}

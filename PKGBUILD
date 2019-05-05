# Maintainer: Robin Lange <robin dot langenc at gmail dot com>
# Contributor: Robin Lange <robin dot langenc at gmail dot com>
pkgname=sleepguard
pkgver=1.0
pkgrel=1
arch=('any')
license=('MIT')
depends=('python' 'python-setuptools' 'python-apscheduler')
makedepends=('python-setuptools')
source=('setup.py' 'sleepguard.py' 'bleep.wav' 'notify-send-all' 'sleepguard.service')
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')
 
build() {
 
  cd "${srcdir}"
  python setup.py build
 
}
 
 
package() {
 
  cd "${srcdir}"
 
  install -Dm644 sleepguard.service "$pkgdir/usr/lib/systemd/system/sleepguard.service"
 
  python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
 
}  

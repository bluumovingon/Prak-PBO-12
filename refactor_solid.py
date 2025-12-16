import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("CheckoutSystem")

# Model Sederhana
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# --- ABSTRAKSI KONTRAK ---
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT ---
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        # Menggunakan logger agar konsisten
        logger.info("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        # Menggunakan logger agar konsisten
        logger.info(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR (SRP & DIP) ---
class CheckoutService:
    """
    Kelas high level untuk mengkoordinasi proses transaksi pembayaran.
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Menginisalisasi CheckoutService dengan depedensi yang diperlukan.

        Args:
        payment_processor (IPaymentProcessor): Implementasi interface pembayaran.
        notifier (INotificationService): Implementasi interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.
        Args:
            order (Order): Objek Pesanan yang akan diproses.
        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """

        #... Logika implentasi disini ...
        pass
        
        logger.info(f"--- Memulai Checkout untuk {order.customer_name} ---")
        
        # Proses Pembayaran
        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order) # Delegasi Notifikasi
            
            # Mengganti print menjadi logger
            logger.info("Checkout Sukses. Transaksi selesai.")
            return True
        return False

# --- PROGRAM UTAMA ---

# Setup Data
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 1. Inject implementasi Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)

print("\n[Skenario 1: Credit Card]") 
checkout_cc.run_checkout(andi_order)

# 2. Pembuktian OCP: Menambah Metode Pembayaran QRIS
class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        logger.info("Payment: Memproses QRIS.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# Inject implementasi QRIS
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)

print("\n[Skenario 2: Pembuktian OCP (QRIS)]")
checkout_qris.run_checkout(budi_order)
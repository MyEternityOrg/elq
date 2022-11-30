import datetime
import os
import platform

if platform.system() == 'Linux':
    import cups
    from fpdf import FPDF
elif platform.system() == 'Windows':
    import win32print
    from win32printing import Printer
else:
    print('Unsupported OS. Exiting....')
    exit(1)


def get_windows_printer_by_name(my_printer: str = 'SAM4S'):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    for pr in printers:
        if str(pr[2]).lower() == my_printer.lower():
            return win32print.OpenPrinter(pr[2])


def create_pdf():
    page_size = tuple([46.0, 60.0])
    pdf = FPDF(format=page_size)
    pdf.set_margins(1, 1, 1)
    pdf.auto_page_break = False
    pdf.add_font('Arial', '', 'app_devices/printer/arial.ttf', uni=True)
    pdf.add_page(orientation='P')
    return pdf


def write_pdf(pdf, offset_y: int = 0, text: str = '', size: int = 8):
    pdf.set_font("Arial", size=size)
    pdf.cell(0, offset_y, txt=text, align='L')
    pdf.set_x(0)
    return pdf


def print_receipt(printer_name: str = 'SAM4S', receipt_id: str = '99999', receipt_count: int = 1,
                  dts: str = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')):
    if platform.system() == 'Linux':
        data = create_pdf()
        write_pdf(data, 3, 'Электронная очередь', 8)
        write_pdf(data, 18, f'#{receipt_id}', 24)
        write_pdf(data, 33, f"{dts}", 8)
        write_pdf(data, 39, '-----------', 8)
        data.output("receipt.pdf")
        conn = cups.Connection()
        print(cups.getServer())
        printers = conn.getPrinters()
        for printer in printers:
            if str(printer).lower() == printer_name.lower():
                for i in range(1, receipt_count + 1):
                    conn.printFile(printer, "receipt.pdf", "document", {"page-left": "1"})
            os.remove("receipt.pdf")

    elif platform.system() == 'Windows':
        printer = get_windows_printer_by_name(printer_name)
        if printer is not None:
            for i in range(1, receipt_count + 1):
                with Printer(printer_name=printer_name) as printer:
                    printer.width = 2048
                    printer.text("Электронная очередь", align="center", font_config={"height": 12})
                    printer.text(f'#{receipt_id}', align="center", font_config={"height": 18})
                    printer.text(f"{dts}", align="center",
                                 font_config={"height": 12})
                    printer.text('-----------')
                    printer.new_page()


if __name__ == "__main__":
    print_receipt('ELLIX50', '1230', 4)

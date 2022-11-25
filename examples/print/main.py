import datetime
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

use_printer = 'SAM4S'


def get_windows_printer_by_name(my_printer: str = 'SAM4S'):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    for pr in printers:
        if pr[2] == my_printer:
            return win32print.OpenPrinter(pr[2])


def create_pdf():
    page_size = tuple([46.0, 60.0])
    pdf = FPDF(format=page_size)
    pdf.set_margins(1, 1, 1)
    pdf.auto_page_break = False
    pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
    pdf.add_page(orientation='P')
    return pdf


def write_pdf(pdf, offset_y: int = 0, text: str = '', size: int = 8):
    pdf.set_font("Arial", size=size)
    pdf.cell(0, offset_y, txt=text, align='L')
    pdf.set_x(0)
    return pdf


def my_printer_function():
    if platform.system() == 'Linux':
        data = create_pdf()
        write_pdf(data, 3, 'Электронная очередь', 8)
        write_pdf(data, 18, '#13333', 24)
        write_pdf(data, 33, f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}", 8)
        write_pdf(data, 39, '-----------', 8)
        data.output("receipt.pdf")
        conn = cups.Connection()
        printers = conn.getPrinters()
        for printer in printers:
            print(f'{printer} {printers[printer]["device-uri"]}')
            printer_name = printers.keys()[0]
            conn.printFile(printer_name, "receipt.pdf", "Python_Status_print", {})

    elif platform.system() == 'Windows':
        printer = get_windows_printer_by_name(use_printer)
        if printer is not None:
            print('Printer found')
            with Printer(printer_name=use_printer) as printer:
                printer.width = 2048
                printer.text("Электронная очередь", align="center", font_config={"height": 12})
                printer.text("#9999", align="center", font_config={"height": 18})
                printer.text(f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}", align="center",
                             font_config={"height": 12})
                printer.text('-----------')
                printer.new_page()


if __name__ == "__main__":
    my_printer_function()

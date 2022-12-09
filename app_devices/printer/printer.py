import datetime
import os
import platform
from fpdf import FPDF
from elq.settings import PRINT_PAPER_W, PRINT_PAPER_H

if platform.system() == 'Linux':
    import cups
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
    page_size = tuple([float(PRINT_PAPER_W), float(PRINT_PAPER_H)])
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


def prepare_print_line(inline: str):
    print_line_ware = str(inline).split(',')[0]
    print_line_count = str(inline).split(',')[1]
    return print_line_ware[
           :PRINT_PAPER_W - 32 - len(print_line_count)].rstrip().lstrip() + '   ' + print_line_count.rstrip().lstrip()


def print_receipt(printer_name: str = 'SAM4S', receipt_id: str = '99999', receipt_count: int = 1,
                  dts: str = datetime.datetime.today().strftime('%Y-%m-%d %H:%M'), wares: list = []):
    print(f'Printing document: {receipt_id} - {receipt_count} times.')
    if platform.system() == 'Linux':
        offset = 42
        data = create_pdf()
        write_pdf(data, 3, 'Электронная очередь', 8)
        write_pdf(data, 18, f'№ {receipt_id}', 32)
        write_pdf(data, 33, f"{dts}", 8)
        if wares is not None:
            for k in wares:
                write_pdf(data, offset, prepare_print_line(k))
                offset += 6
        write_pdf(data, offset + 6, 'Приятного аппетита :)', 8)
        write_pdf(data, offset + 12, '______________________', 8)
        data.output(f"{printer_name}_receipt.pdf")
        conn = cups.Connection()
        print(cups.getServer())
        printers = conn.getPrinters()
        for printer in printers:
            print(f'Cups printer: {printer}, input name printer {printer_name}')
            if str(printer).lower() == printer_name.lower():
                for i in range(1, receipt_count + 1):
                    conn.printFile(printer, f"{printer_name}_receipt.pdf", "document", {"page-left": "1"})
                if os.path.exists(f"{printer_name}_receipt.pdf"):
                    os.remove(f"{printer_name}_receipt.pdf")

    elif platform.system() == 'Windows':
        printer = get_windows_printer_by_name(printer_name)
        if printer is not None:
            for i in range(1, receipt_count + 1):
                with Printer(printer_name=printer_name) as printer:
                    printer.width = 2048
                    printer.text("Электронная очередь", align="center", font_config={"height": 12})
                    printer.text(f'№ {receipt_id}', align="center", font_config={"height": 24})
                    printer.text(f"{dts}", align="center", font_config={"height": 12})
                    if wares is not None:
                        for k in wares:
                            printer.text(k, align="center", font_config={"height": 12})
                    printer.text("Приятного аппетита :)", align="center",
                                 font_config={"height": 12})
                    printer.text('-----------')
                    printer.new_page()


if __name__ == "__main__":
    cpath = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
    path = cpath + 'arial.ttf'
    int_printer_name = 'p1'
    doc = FPDF(format=tuple([float(PRINT_PAPER_W), float(PRINT_PAPER_H)]))
    doc.set_margins(1, 1, 1)
    doc.auto_page_break = False
    doc.add_font('Arial', '', f'{path}', uni=True)
    doc.add_page(orientation='P')
    offset = 42
    write_pdf(doc, 3, 'Электронная очередь', 8)
    write_pdf(doc, 18, f'№ 999999', 32)
    write_pdf(doc, 33, f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M')}", 8)
    for k in [
        'Очень длинное тестовое наименование товара товара, 9999.0',
        'Длинное тестовое наименование товара, 666.0',
        'Среднее наименование товара, 66.0',
        'Короткое имя товара, 1.0'
    ]:
        write_pdf(doc, offset, prepare_print_line(k))
        offset += 6
    write_pdf(doc, offset + 6, 'Приятного аппетита :)', 8)
    write_pdf(doc, offset + 12, '-----------', 8)
    doc.output(f"{cpath}{int_printer_name}_receipt.pdf")
    conn = cups.Connection()
    print(cups.getServer())
    printers = conn.getPrinters()
    for printer in printers:
        print(f'Cups printer: {printer}, input name printer {int_printer_name}')
        if str(printer).lower() == int_printer_name.lower():
            for i in range(1, int_printer_name + 1):
                conn.printFile(printer, f"{cpath}{int_printer_name}_receipt.pdf", "document", {"page-left": "1"})
        if os.path.exists(f"{cpath}{int_printer_name}_receipt.pdf"):
            os.remove(f"{cpath}{int_printer_name}_receipt.pdf")

from base64 import encode
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import conf
from fpdf import FPDF
import os
import matplotlib.pyplot as plt


PATH = os.path.abspath(".")

def revision_periodica():
    accesos = 0
    warnings = 0
    errores = 0
    w = False 
    e= False

    file = open(conf.LOGS, "r").readlines()

    with open(conf.LOGS, 'r') as f:
        ultimalinea = f.readlines()[-1]
        fecha=ultimalinea.split(" ")[0].split("/",1)[1]

    for line in reversed(file):
        if fecha in line : 
            accesos+=1
            if (line.split(" ")[2]== "Warning(s)") and (w == False):
                warnings = int(line.split(" ")[4]); w = True
            elif (line.split(" ")[2]) == "Error(s)" and (e == False):
                errores = int(line.split(" ")[4]); e = True

    craftea_grafico(accesos,errores,warnings,fecha)
    craftea_pdf(fecha,str(accesos),str(errores),str(warnings))
    craftea_email(fecha)

def craftea_grafico(accesos,errores,warnings,fecha):
    accesos_normales= accesos-(errores+warnings)
    valores = [accesos_normales]
    legend = ["accesos sin incidencia"]
    etiquetas=[str(accesos_normales)]
    explode=[0]

    if(errores!=0):valores.append(errores);legend.append("errores de autenticacion");explode.append(0.2);etiquetas.append(str(errores))
    if(warnings!=0):valores.append(warnings);legend.append("warnings");explode.append(0.2);etiquetas.append(str(warnings))

    etiquetas = tuple(etiquetas)
    f1={"family": "arial","color": "black", "size": 20, "fontweight": "roman"}
    
    plt.figure(figsize=(7,3))
    plt.pie(valores,startangle=90,shadow=True, explode=explode, autopct="%2.2f%%")
    plt.title("Accesos al Sistema de Archivos\n",fontdict=f1)
    plt.legend(legend,loc="upper left",fontsize="x-small")
    plt.axis("equal")
    plt.savefig(os.path.join(PATH,"revisiones","graficos","grafico"+fecha.replace("/","-")+".png"),bbox_inches='tight',dpi=300)

def craftea_pdf(fecha,accesos,errores,warnings):
    porcentaje = (int(errores)+int(warnings))/int(accesos)

    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 40)
    pdf.cell(200, 10, txt = "HIDS",ln = 1, align = 'C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt = "Reporte "+fecha+"\n\n" ,ln = 1, align = 'C')
    pdf.image(os.path.join(PATH,"revisiones","graficos","grafico"+fecha.replace("/","-")+".png"),20,40, h=100,w=180)
    pdf.cell(200, 120, txt = "",ln = 1, align = 'L')
    pdf.set_left_margin(32)
    pdf.set_font("Arial",style="")
    pdf.cell(200, 10, txt = "· Nº de errores detectados: "+errores,ln = 1, align = 'L')
    pdf.cell(200, 10, txt = "· Nº de warnings detectados: "+warnings,ln = 1, align = 'L')
    pdf.cell(200, 10, txt = "· Nº total de accesos: "+accesos,ln = 1, align = 'L')
    pdf.cell(200, 10, txt = "· Incidencia = errores + warnings + errores_auth",ln = 1, align = 'L')
    pdf.cell(200, 10, txt = "· Porcentaje de incidencias (errores): "+str("{:%}".format(porcentaje)),ln = 1, align = 'L')
    pdf.output(os.path.join(PATH,"revisiones", "reporte-"+fecha.replace("/","-")+".pdf"), 'F')

def craftea_email(fecha):

    fecha_arreglada = fecha.replace("/","-")
    ruta = os.path.join(PATH,"revisiones", "reporte-"+str(fecha_arreglada)+".pdf")
    
    mensaje = MIMEMultipart()
    mensaje["From"]= "correo@hids.pai"
    mensaje["To"]= "sysadmin@hids.com"
    mensaje["Subject"]= "Reporte de accesos HIDS "+fecha
    mensaje_texto = MIMEText("Se adjunta el archivo pdf con el reporte de accesos. \n Le enviamos un Cordial saludo.")
    mensaje.attach(mensaje_texto)

    pdfname= "reporte-"+fecha_arreglada+".pdf"
    pdf = open(ruta, "rb")
    payload = MIMEBase("application","octate-stream",Name = pdfname )
    payload.set_payload(pdf.read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    mensaje.attach(payload)

    conexion = smtplib.SMTP(host="localhost",port= 2500)
    conexion.sendmail(from_addr="correo@hids.pai", to_addrs="sysadmin@hids.com",msg=mensaje.as_string())
    conexion.quit()
    

revision_periodica()
import flet as ft

def main (page):
    titulo = ft.Text("MessagePy")
    chat = ft.Column()
    nomeUsuario = ft.TextField(label="Insira o seu nome:")


    def tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size=12, italic=True, color=ft.colors.ORANGE_500))
        page.update()

    page.pubsub.subscribe(tunel)


    def enviarMensagem(evento):
        page.pubsub.send_all({"texto": campoMensagem.value, "usuario": nomeUsuario.value, "tipo": "mensagem"})
        campoMensagem.value = ""
        page.update()

    campoMensagem = ft.TextField(label="Mensagem:", on_submit=enviarMensagem)
    botaoEnviarMensagem = ft.ElevatedButton("Enviar", on_click=enviarMensagem)


    def entrarPopup(evento):
        page.pubsub.send_all({"usuario": nomeUsuario.value, "tipo": "entrada"})
        # limpa a tela inicial
        popup.open = False
        page.remove(titulo)
        page.remove(iniciar)

        # adiciona chat e botão enviar
        page.add(chat)
        page.add(ft.Row([campoMensagem , botaoEnviarMensagem]))
        page.update()


    popup = ft.AlertDialog(
        open = False,
        modal = True,
        title = ft.Text("Bem vindo ao MessagePy"),
        content= nomeUsuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrarPopup)]
    )
    def entrarChat(evento):
        page.dialog = popup
        popup.open=True
        page.update()

    iniciar = ft.ElevatedButton("Start Chat", on_click=entrarChat)


    page.add(titulo)
    page.add(iniciar)

ft.app(target = main, port=8000)
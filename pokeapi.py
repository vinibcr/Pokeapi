import requests
import tkinter as tk
from tkinter import messagebox, PhotoImage

# Função para obter os tipos de um Pokémon específico usando seu nome ou número
def obter_tipos_pokemon(nome_ou_numero):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome_ou_numero.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        nome = pokemon_data['name']
        tipos = [tipo['type']['name'] for tipo in pokemon_data['types']]
        image_url = pokemon_data['sprites']['front_default']
        return nome.capitalize(), tipos, image_url
    else:
        return None, None, None

# Função para obter todos os Pokémon de um tipo específico
def obter_pokemons_por_tipo(tipo):
    url = f"https://pokeapi.co/api/v2/type/{tipo.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        tipo_data = response.json()
        pokemons = [pokemon['pokemon']['name'] for pokemon in tipo_data['pokemon']]
        return pokemons
    else:
        return []

# Função chamada ao pressionar o botão "Verificar Tipo"
def verificar_tipo_pokemon():
    nome_ou_numero = entry_pokemon.get()
    if nome_ou_numero:
        nome, tipos, image_url = obter_tipos_pokemon(nome_ou_numero)
        if nome and tipos:
            exibir_imagem_pokemon(image_url)
            label_tipos.config(text=f"Tipos: {', '.join(tipos)}")  # Atualiza o texto do label com os tipos
            label_nome.config(text=f"Nome: {nome}")  # Atualiza o texto do label com o nome do Pokémon
        else:
            messagebox.showerror("Erro", f"Pokémon '{nome_ou_numero}' não encontrado.")
            label_tipos.config(text="")  # Limpa o label de tipos em caso de erro
            label_nome.config(text="")  # Limpa o label de nome em caso de erro
    else:
        messagebox.showwarning("Atenção", "Por favor, insira o nome ou número de um Pokémon.")

# Função chamada ao pressionar o botão "Listar Pokémon por Tipo"
def listar_pokemons_por_tipo():
    tipo = entry_tipo.get()
    if tipo:
        pokemons = obter_pokemons_por_tipo(tipo)
        if pokemons:
            messagebox.showinfo("Resultado", f"Pokémons do tipo {tipo.capitalize()}: {', '.join(pokemons)}")
        else:
            messagebox.showerror("Erro", f"Tipo '{tipo}' não encontrado ou sem Pokémons.")
    else:
        messagebox.showwarning("Atenção", "Por favor, insira um tipo de Pokémon.")

# Função para exibir a imagem do Pokémon
def exibir_imagem_pokemon(url):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            with open("pokemon_image.gif", "wb") as file:
                file.write(response.content)
            imagem = PhotoImage(file="pokemon_image.gif")
            label_imagem.configure(image=imagem)
            label_imagem.image = imagem
        else:
            messagebox.showerror("Erro", "Não foi possível carregar a imagem do Pokémon.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Verificador de Tipos de Pokémon")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Entrada e botão para verificar o tipo de um Pokémon específico
label_pokemon = tk.Label(frame, text="Nome ou Número do Pokémon:")
label_pokemon.grid(row=0, column=0, sticky="e")

entry_pokemon = tk.Entry(frame)
entry_pokemon.grid(row=0, column=1)

btn_verificar_tipo = tk.Button(frame, text="Verificar Tipo", command=verificar_tipo_pokemon)
btn_verificar_tipo.grid(row=0, column=2, padx=5, pady=5)

# Entrada e botão para listar todos os Pokémon de um tipo específico
label_tipo = tk.Label(frame, text="Tipo de Pokémon:")
label_tipo.grid(row=1, column=0, sticky="e")

entry_tipo = tk.Entry(frame)
entry_tipo.grid(row=1, column=1)

btn_listar_pokemons = tk.Button(frame, text="Listar Pokémon por Tipo", command=listar_pokemons_por_tipo)
btn_listar_pokemons.grid(row=1, column=2, padx=5, pady=5)

# Label para exibir a imagem do Pokémon
label_imagem = tk.Label(root)
label_imagem.pack(pady=10)

# Labels para exibir o nome e os tipos do Pokémon
label_nome = tk.Label(root, text="", font=("Arial", 14))
label_nome.pack(pady=5)

label_tipos = tk.Label(root, text="", font=("Arial", 14))
label_tipos.pack(pady=5)

# Loop principal da interface gráfica
root.mainloop()

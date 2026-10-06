import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Tabela4.csv", sep=";", decimal=",")
df = df.dropna(axis=1, how="all")

print("Tabela original:")
print(df.head())

anos = [c for c in df.columns if str(c).isdigit()]
print("\nAnos disponíveis:")
print(anos)

id_vars = [c for c in df.columns if c not in anos]

df_longo = df.melt(
    id_vars=id_vars,
    value_vars=anos,
    var_name="Ano",
    value_name="IDH",
)

df_longo["Ano"] = df_longo["Ano"].astype(int)
df_longo["IDH"] = pd.to_numeric(df_longo["IDH"], errors="coerce")

print("\nTabela no formato longo:")
print(df_longo.head())

df_ordenado = df.sort_values("2023", ascending=False)

print("\nEstados ordenados pelo IDH de 2023:")
print(df_ordenado[["Sigla", "Estado", "2023"]])

df["melhora_1991_2023"] = df["2023"] - df["1991"]

melhor_estado = df.loc[df["melhora_1991_2023"].idxmax()]

print("\nEstado com maior melhora entre 1991 e 2023:")
print("Estado:", melhor_estado["Estado"])
print("Sigla:", melhor_estado["Sigla"])
print("IDH em 1991:", melhor_estado["1991"])
print("IDH em 2023:", melhor_estado["2023"])
print("Melhora:", melhor_estado["melhora_1991_2023"])

piorados = df[df["2023"] < df["1991"]]

print("\nEstados que tiveram piora:")

if piorados.empty:
    print("Nenhum estado apresentou piora do IDH.")
else:
    print(piorados[["Sigla", "Estado", "1991", "2023"]])

mg = df_longo[df_longo["Sigla"] == "MG"].sort_values("Ano")

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    mg["Ano"],
    mg["IDH"],
    marker="o",
    linewidth=1.8
)

ax.set_title("Evolução do IDH de Minas Gerais")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
ax.set_ylim(0.3, 0.9)

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(12, 7))

for sigla, grupo in df_longo.groupby("Sigla"):
    grupo = grupo.sort_values("Ano")
    
    ax.plot(
        grupo["Ano"],
        grupo["IDH"],
        marker="o",
        markersize=3,
        linewidth=1.5,
        label=sigla
    )

ax.set_title("Evolução do IDH por estado (1991–2023)")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
ax.set_ylim(0.3, 0.9)

ax.legend(
    ncol=3,
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    title="UF"
)

fig.tight_layout()
plt.show()
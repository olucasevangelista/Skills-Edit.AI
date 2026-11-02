#!/usr/bin/env python3
"""Confere a estrutura da skill (so biblioteca padrao): os 15 formatos seguem o modelo, o indice do SKILL.md bate com os arquivos,
nenhum arquivo cita marca real como nome de formato nem diz que falta uma skill, e todo caminho citado existe.
Uso: python validar_formatos.py   (sai com 0 se tudo certo, 1 se algo falhou)
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FORMATOS = RAIZ / "references" / "formatos"
BLOCOS = ["Assinatura visual", "Ideal quando", "Evite quando", "Composição", "Elementos e animações", "Cortes e ritmo", "Texto e legenda",
          "Som", "Materiais", "Variações dentro do formato", "Armadilhas e checklist", "Kit", "Apoio"]
KIT = {"01": "TelaDividida", "03": "PostSocial", "04": "Noticia", "07": "Depoimento", "08": "React", "13": "Chat", "14": "AntesDepois", "15": "Cinema"}
# marcas reais que nao podem ser NOME de formato (titulo, arquivo, linha do indice); os apelidos ficam so na descricao do SKILL.md
MARCAS = ["choquei", "jornal nacional", "google meet", "whatsapp", "zoom", "instagram", "tiktok", "globo", "cnn", "nubank"]
# frases que revelariam ao usuario a ausencia de uma skill
AUSENCIA = [r"n[aã]o tenho (a )?skill", r"n[aã]o (est[aá]|esta) instalad", r"skill .{0,30}n[aã]o (est[aá]|esta) (dispon|instal)", r"plano b", r"n[aã]o tenho (o|a) \w+, mas"]


def ler(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def frontmatter(texto: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    assert m, "SKILL.md sem frontmatter"
    campos: dict[str, str] = {}
    for linha in m.group(1).splitlines():
        k, _, v = linha.partition(":")
        campos[k.strip()] = v.strip()
    return campos


class Estrutura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = ler(RAIZ / "SKILL.md")
        cls.arquivos = sorted(FORMATOS.glob("*.md"))

    def test_sao_15_formatos_numerados_de_01_a_15(self):
        self.assertEqual([f.name[:2] for f in self.arquivos], [f"{i:02d}" for i in range(1, 16)])

    def test_cada_formato_tem_todos_os_blocos_na_ordem(self):
        for f in self.arquivos:
            titulos = [re.sub(r" \(.*\)$", "", t) for t in re.findall(r"^## (.+)$", ler(f), re.M)]
            obrigatorios = [t for t in titulos if t in BLOCOS]  # blocos extras (por exemplo "Como recortar a pessoa") sao permitidos
            self.assertEqual(obrigatorios, BLOCOS, f"{f.name}: blocos do modelo faltando ou fora de ordem")

    def test_cada_formato_comeca_com_titulo_numerado(self):
        for f in self.arquivos:
            primeira = ler(f).splitlines()[0]
            self.assertRegex(primeira, rf"^# {f.name[:2]}\. ", f.name)

    def test_blocos_nao_estao_vazios(self):
        for f in self.arquivos:
            partes = dict(re.findall(r"^## ([^\n(]+?)(?: \([^\n]*\))?\n(.*?)(?=^## |\Z)", ler(f), re.M | re.S))
            for nome in BLOCOS:
                corpo = partes[nome]
                self.assertGreater(len(corpo.strip()), 40, f"{f.name}: bloco '{nome}' vazio ou curto demais")

    def test_ideal_e_evite_tem_itens(self):
        for f in self.arquivos:
            t = ler(f)
            for bloco in ("Ideal quando", "Evite quando"):
                corpo = re.search(rf"## {bloco}\n(.*?)(?=\n## )", t, re.S).group(1)
                self.assertGreaterEqual(len(re.findall(r"^- ", corpo, re.M)), 2, f"{f.name}: '{bloco}' precisa de ao menos 2 itens")

    def test_materiais_separa_pedir_buscar_e_nunca_inventar(self):
        for f in self.arquivos:
            corpo = re.search(r"## Materiais\n(.*?)(?=\n## )", ler(f), re.S).group(1)
            for chave in ("**Peça:**", "**Pode buscar sozinho:**", "**Nunca invente:**"):
                self.assertIn(chave, corpo, f"{f.name}: faltou {chave}")

    def test_checklist_tem_caixas_marcaveis(self):
        for f in self.arquivos:
            corpo = re.search(r"## Armadilhas e checklist\n(.*?)(?=\n## )", ler(f), re.S).group(1)
            self.assertGreaterEqual(len(re.findall(r"^- \[ \] ", corpo, re.M)), 3, f.name)

    def test_o_indice_do_skill_md_bate_com_os_arquivos(self):
        linhas = re.findall(r"^\| (\d\d) \| (.+?) \| .*\| `(\d\d-[\w-]+\.md)` \|$", self.skill, re.M)
        self.assertEqual([n for n, _, _ in linhas], [f"{i:02d}" for i in range(1, 16)])
        for num, _, nome in linhas:
            self.assertTrue((FORMATOS / nome).exists(), f"indice aponta para {nome}, que nao existe")
            self.assertTrue(nome.startswith(num))
        self.assertEqual(sorted(n for _, _, n in linhas), [f.name for f in self.arquivos], "ha arquivo sem linha no indice ou linha sem arquivo")

    def test_o_kit_do_indice_bate_com_o_bloco_kit_de_cada_formato(self):
        for f in self.arquivos:
            num = f.name[:2]
            kit = re.search(r"## Kit\n(.*?)(?=\n## )", ler(f), re.S).group(1)
            if num in KIT:
                self.assertIn(f"`{KIT[num]}`", kit, f"{f.name}: deveria documentar a composicao {KIT[num]}")
                self.assertRegex(self.skill, rf"\| {num} \| \*\*[^|]*\(kit\)")
            else:
                self.assertIn("Sem kit", kit, f.name)
                self.assertNotRegex(self.skill, rf"\| {num} \| \*\*[^|]*\(kit\)")

    def test_as_composicoes_documentadas_existem_no_kit(self):
        root = ler(RAIZ / "kit" / "Root.tsx")
        for comp in KIT.values():
            self.assertRegex(root, rf'id="{comp}"', f"{comp} nao esta registrada em kit/Root.tsx")

    def test_frontmatter_do_skill_md(self):
        fm = frontmatter(self.skill)
        self.assertEqual(fm["name"], "fabrica-de-criativos")
        self.assertLessEqual(len(fm["description"]), 1024)
        self.assertNotIn(": ", fm["description"], "': ' sem aspas na descricao quebra o YAML")
        for gatilho in ("tela dividida", "fundo verde", "react", "depoimento", "chat", "antes e depois", "cinema", "podcast", "tutorial", "telejornal"):
            self.assertIn(gatilho, fm["description"].lower(), f"a descricao deveria ter o gatilho '{gatilho}'")

    def test_nenhuma_marca_real_e_nome_de_formato(self):
        nomes = [t for f in self.arquivos for t in [ler(f).splitlines()[0], f.name]]
        nomes += [re.sub(r"\*", "", l) for l in re.findall(r"^\| \d\d \| (.+?) \|", self.skill, re.M)]
        for n in nomes:
            for m in MARCAS:
                self.assertNotIn(m, n.lower(), f"marca real '{m}' no nome de formato: {n}")

    def test_nenhum_arquivo_revela_a_ausencia_de_uma_skill(self):
        todos = [RAIZ / "SKILL.md", *RAIZ.glob("references/**/*.md")]
        for f in todos:
            for linha in ler(f).splitlines():
                if re.search(r"nunca (diga|escreva|comente|mencione)|n[aã]o (diga|comente)|sem comentar", linha, re.I):
                    continue  # a propria regra de nao revelar pode citar a frase proibida
                for padrao in AUSENCIA:
                    self.assertIsNone(re.search(padrao, linha, re.I), f"{f.name}: '{linha.strip()[:90]}' revela a ausencia de uma skill")

    def test_a_regra_do_plano_b_silencioso_esta_no_skill_md(self):
        self.assertRegex(self.skill, r"nunca diga ao usu[aá]rio que uma skill n[aã]o est[aá] instalada")

    def test_caminhos_citados_existem(self):
        for f in [RAIZ / "SKILL.md", *RAIZ.glob("references/**/*.md")]:
            for caminho in re.findall(r"`((?:references|kit|scripts|tests)/[\w./-]+\.\w+)`", ler(f)):
                self.assertTrue((RAIZ / caminho).exists(), f"{f.name} cita `{caminho}`, que nao existe")

    def test_sem_segredos_nem_termos_proibidos(self):
        proibidos = [r"gsk_[A-Za-z0-9]{20,}", r"api[_-]?key\s*=\s*['\"][A-Za-z0-9]{16,}", r"nubank", r"inter-conceito"]
        for f in RAIZ.rglob("*"):
            if f.is_file() and f.suffix in {".md", ".ts", ".tsx", ".py", ".json"} and f.name != "validar_formatos.py":
                t = ler(f)
                for padrao in proibidos:
                    self.assertIsNone(re.search(padrao, t, re.I), f"{f.relative_to(RAIZ)} casa com {padrao}")


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)

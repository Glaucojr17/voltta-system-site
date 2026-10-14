from pathlib import Path
import unittest
from html.parser import HTMLParser
BASE=Path(__file__).resolve().parents[1]/"modelos"
SEGMENTS=["institucional","loja-virtual","landing-page","portfolio","catalogo-online","cardapio-digital"]
class Parser(HTMLParser):
 def __init__(self):
  super().__init__()
  self.refs=[]
  self.h1=0
  self.lang=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="html":self.lang=a.get("lang")=="pt-BR"
  if tag=="h1":self.h1+=1
  for attr in ("href","src"):
   value=a.get(attr)
   if value and not (value.startswith("#") or value.startswith("http") or value.startswith("mailto:") or value.startswith("tel:")):self.refs.append(value)
class TestModels(unittest.TestCase):
 def test_pages_and_local_assets(self):
  for name in ["",*SEGMENTS]:
   with self.subTest(page=name or "hub"):
    path=BASE/name/"index.html"
    self.assertTrue(path.is_file())
    parser=Parser();parser.feed(path.read_text())
    self.assertTrue(parser.lang)
    self.assertEqual(parser.h1,1)
    for ref in parser.refs:
     ref=ref.split("#")[0].split("?")[0]
     if ref:
      resolved=(path.parent/ref).resolve()
      self.assertTrue(resolved.is_relative_to(BASE.resolve()),ref)
      if resolved.is_dir():resolved/= "index.html"
      self.assertTrue(resolved.is_file(),f"{path}: {ref}")
if __name__=="__main__":unittest.main()

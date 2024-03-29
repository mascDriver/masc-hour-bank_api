# Nome do projeto

<!---Esses são exemplos. Veja https://shields.io para outras pessoas ou para personalizar este conjunto de escudos. Você pode querer incluir dependências, status do projeto e informações de licença aqui--->

![GitHub repo size](https://img.shields.io/github/repo-size/mascdriver/masc-hour-bank_api?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/mascdriver/masc-hour-bank_api?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/mascdriver/masc-hour-bank_api?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/mascdriver/masc-hour-bank_api?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/mascdriver/masc-hour-bank_api?style=for-the-badge)


> Projeto em desenvolvimento

## 🚀 Instalando dependencias

Para instalar o masc-hour-bank_api, siga estas etapas:

Linux e macOS:
```
python -m pip install -r requirements.tst
python manage.py migrate
```


## ☕ Usando

Para usar masc-hour-bank_api, siga estas etapas:

```
python manage.py runserver
```

Também é necessário adicionar as horas para que o sistema tenha onde se basear, basta seguir esses passos
```python
import pandas
time_range = pandas.date_range('2022-08-02T00:00:00.000Z', '2022-08-02T23:59:00.000Z', freq='T')
from attendance.models import AttendanceHour
for time in time_range.time:
    AttendanceHour.objects.get_or_create(hour=time)
```


## 📫 Contribuindo para Masc Hour Bank_api
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com masc-hour-bank_api, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin masc-hour-bank_api/<local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/31291734?v=4" width="100px;" alt="Foto do Iuri Silva no GitHub"/><br>
        <sub>
          <b>Diogo Baltazar</b>
        </sub>
      </a>
    </td>
  </tr>
</table>


## 😄 Seja um dos contribuidores<br>

Quer fazer parte desse projeto? Clique [AQUI](CONTRIBUTING.md) e leia como contribuir.

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#nome-do-projeto)<br>
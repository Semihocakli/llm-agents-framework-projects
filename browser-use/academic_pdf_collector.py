from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import os
import requests
from urllib.parse import urljoin


async def academic_pdf_downloader():
    task = """Adımları uygula:
    1. https://arxiv.org adresine git
    2. Arama çubuğuna "neural networks 2024" yaz
    3. "Date Posted" filtresinden "2024" seç
    4. İlk 5 makalenin başlık ve URL'lerini çıkar
    5. Her makalenin PDF linkini bul
    6. PDF'leri "makaleler" klasörüne indir
    """

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    agent = Agent(
        task=task,
        llm=model,
    )

    try:
        # Makaleler klasörünü oluştur
        os.makedirs("makaleler", exist_ok=True)

        # Tarayıcı otomasyonunu başlat
        history = await agent.run()
        result = history.final_result()

        if result:
            # JSON çıktısını parse et
            data = eval(result.replace("'", '"'))  # Basit JSON dönüşümü
            for item in data.get("makaleler", []):
                pdf_url = urljoin("https://arxiv.org", item["pdf_url"])
                response = requests.get(pdf_url)

                if response.status_code == 200:
                    filename = f"makaleler/{item['baslik'].replace(' ', '_')}.pdf"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f" İndirildi: {filename}")
                else:
                    print(f" Hata: {item['baslik']} indirilemedi")

    except Exception as e:
        print(f" Kritik Hata: {str(e)}")


if __name__ == '__main__':
    asyncio.run(academic_pdf_downloader())
from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller, ActionResult, Browser
import asyncio
import os

controller = Controller()

@controller.action("Kullanıcıdan CAPTCHA Al")
def get_captcha_from_user(question: str) -> str:
    """CAPTCHA'yı kullanıcıya göster ve cevabını al"""
    print(f"\n️ Lütfen e-Okul giriş sayfasındaki CAPTCHA'yı görüntüleyin.")
    return input("CAPTCHA Metni: ").strip()

@controller.action("Kullanıcıdan Bilgileri Al")
def get_credentials() -> dict:
    """Kullanıcı adı ve şifreyi kullanıcıdan al"""
    print("\n e-Okul Giriş Bilgilerinizi Girin:")
    username = input("Kullanıcı Adı (TC Kimlik No): ").strip()
    password = input("Şifre: ").strip()
    return {"username": username, "password": password}


async def main():
    llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    agent = Agent(
        task="""Adımları takip et:
        1. https://eokulyd.meb.gov.tr adresine git
        2. CAPTCHA görüntüsünü bul ve "Kullanıcıdan CAPTCHA Al" eylemiyle çöz
        3. "Kullanıcıdan Bilgileri Al" eylemiyle kullanıcı adı ve şifreyi al
        4. Forma TC Kimlik No, şifre ve CAPTCHA'yı gir
        5. "Giriş Yap" butonuna tıkla
        6. Giriş başarılıysa "Hoşgeldiniz" mesajını kontrol et
        """,
        llm=llm,
        use_vision=True,
    )

    result = await agent.run()
    print(f"\n Sonuç: {result}")


if __name__ == "__main__":
    asyncio.run(main())
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def translate_text(
    text: str | bytes | list[str] = "¡Hola amigos y amigas!",
    target_language: str = "en",
    source_language: str | None = None,
    credentials: dict[str, str] | None = None,
) -> dict:
    """Translates a given text into the specified target language.

    Find a list of supported languages and codes here:
    https://cloud.google.com/translate/docs/languages#nmt

    Args:
        text: The text to translate. Can be a string, bytes or a list of strings.
              If bytes, it will be decoded as UTF-8.
        target_language: The ISO 639 language code to translate the text into
                         (e.g., 'en' for English, 'es' for Spanish).
        source_language: Optional. The ISO 639 language code of the input text
                         (e.g., 'fr' for French). If None, the API will attempt
                         to detect the source language automatically.
        credentials: Optional. The OAuth2 Credentials to use for this client

    Returns:
        A dictionary containing the translation results.
    """

    from google.cloud import translate_v2 as translate

    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, bytes):
        text = [text.decode("utf-8")]

    if isinstance(text, str):
        text = [text]

    # If a string is supplied, a single dictionary will be returned.
    # In case a list of strings is supplied, this method
    # will return a list of dictionaries.

    # Find more information about translate function here:
    # https://cloud.google.com/python/docs/reference/translate/latest/google.cloud.translate_v2.client.Client#google_cloud_translate_v2_client_Client_translate
    results = translate_client.translate(
        values=text,
        target_language=target_language,
        source_language=source_language
    )

    for result in results:
        if "detectedSourceLanguage" in result:
            logger.info(f"Detected source language: {result['detectedSourceLanguage']}")

        logger.info(f"Input text: {result['input']}")
        logger.info(f"Translated text: {result['translatedText']}")

    return results

if __name__ == "__main__":
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('translate-api-python.json')

    # print(translate_text("Bingenbash lo eni theatres unay", source_language="te"))
    translate_text("nuvu evaru?", credentials=credentials)
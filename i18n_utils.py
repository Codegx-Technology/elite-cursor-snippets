from babel import Locale
from babel.messages.pofile import read_po
from typing import Dict, Any, Optional
from config_loader import get_config
from logging_setup import get_logger
from functools import lru_cache
import os
from unittest.mock import MagicMock # Elite Cursor Snippet: MagicMock_import

logger = get_logger(__name__)
config = get_config()

# Placeholder for loaded translations
_translations: Dict[str, Dict[str, str]] = {}

def load_translations(lang_code: str):
    """
    Loads translations for a given language code.
    // [TASK]: Load translations from .po files
    // [GOAL]: Provide translated strings for the application
    // [ELITE_CURSOR_SNIPPET]: doccode
    """
    if lang_code in _translations:
        return _translations[lang_code]

    translations_dir = os.path.join(os.path.dirname(__file__), "translations")
    locale_dir = os.path.join(translations_dir, lang_code, "LC_MESSAGES")
    po_file_path = os.path.join(locale_dir, "messages.po")

    if not os.path.exists(po_file_path):
        logger.warning(f"Translation file not found for {lang_code} at {po_file_path}. Using default.")
        return {}

    try:
        with open(po_file_path, "r", encoding="utf-8") as f:
            catalog = read_po(f)
            _translations[lang_code] = {message.id: str(message.string) for message in catalog}
            logger.info(f"Loaded {len(_translations[lang_code])} translations for {lang_code}.")
            return _translations[lang_code]
    except Exception as e:
        logger.error(f"Failed to load translations for {lang_code}: {e}")
        return {}

@lru_cache(maxsize=128)
def gettext(message_id: str, locale: str = "en", **variables: Any) -> str:
    """
    Translates a message ID into the target locale.
    // [TASK]: Translate a message ID
    // [GOAL]: Provide a simple translation function
    // [ELITE_CURSOR_SNIPPET]: doccode
    """
    translations = load_translations(locale)
    translated_message = translations.get(message_id, message_id) # Fallback to message_id if not found

    # Apply variables if any
    if variables:
        try:
            return translated_message.format(**variables)
        except KeyError as e:
            logger.warning(f"Missing variable {e} in translation for '{message_id}' ({locale}).")
            return translated_message # Return untranslated if variables don't match
    return translated_message

def get_locale_from_request(request: Any) -> str:
    """
    Detects the preferred locale from the request (e.g., Accept-Language header).
    // [TASK]: Detect locale from request
    // [GOAL]: Determine the user's preferred language
    // [ELITE_CURSOR_SNIPPET]: aihandle
    """
    # Placeholder for tenant-specific locale from DB
    # tenant_id = request.state.tenant_id # Assuming tenant_id is set in request.state
    # tenant_locale = get_tenant_locale_from_db(tenant_id) # This function would query DB
    # if tenant_locale:
    #     return tenant_locale

    # Fallback to Accept-Language header
    accept_language = request.headers.get("Accept-Language")
    if accept_language:
        try:
            # Parse Accept-Language header (e.g., "en-US,en;q=0.9,fr;q=0.8")
            locales = Locale.parse(accept_language, sep=',')
            # Return the first preferred language that we support
            supported_languages = config.i18n.supported_languages # e.g., ["en", "sw", "fr"]
            for locale in locales:
                if locale.language in supported_languages:
                    return locale.language
        except Exception as e:
            logger.warning(f"Failed to parse Accept-Language header: {e}")
    
    return config.i18n.default_language # Default language from config

# Placeholder for tenant-specific locale from DB (needs actual DB integration)
def get_tenant_locale_from_db(tenant_id: str) -> Optional[str]:
    """
    Simulates fetching tenant-specific locale from a database.
    // [TASK]: Fetch tenant locale from DB
    // [GOAL]: Provide tenant-specific language preference
    // [ELITE_CURSOR_SNIPPET]: doccode
    """
    # In a real application, this would query your database for the tenant's preferred locale.
    # For demonstration, we return None, meaning no tenant-specific override.
    return None

# Example usage (for testing)
if __name__ == "__main__":
    # Create dummy translation files for testing
    os.makedirs("translations/en/LC_MESSAGES", exist_ok=True)
    with open("translations/en/LC_MESSAGES/messages.po", "w", encoding="utf-8") as f:
        f.write("""
msgid "hello_world"
msgstr "Hello, World!"

msgid "welcome_user"
msgstr "Welcome, {name}!"
""")
    os.makedirs("translations/sw/LC_MESSAGES", exist_ok=True)
    with open("translations/sw/LC_MESSAGES/messages.po", "w", encoding="utf-8") as f:
        f.write("""
msgid "hello_world"
msgstr "Habari, Dunia!"

msgid "welcome_user"
msgstr "Karibu, {name}!"
""")
    
    # Mock config for testing
    class MockI18nConfig:
        supported_languages = ["en", "sw", "fr"]
        default_language = "en"
    class MockConfig:
        i18n = MockI18nConfig()
    
    # Temporarily override global config for testing
    original_config = config
    config = MockConfig()

    print(f"English: {gettext('hello_world', locale='en')}")
    print(f"Swahili: {gettext('hello_world', locale='sw')}")
    print(f"English (with var): {gettext('welcome_user', locale='en', name='Alice')}")
    print(f"Swahili (with var): {gettext('welcome_user', locale='sw', name='Bob')}")
    print(f"Unknown: {gettext('unknown_message', locale='en')}")

    # Mock a request object
    class MockRequest:
        def __init__(self, headers: Dict[str, str]):
            self.headers = headers
            self.state = MagicMock() # For request.state.tenant_id

    mock_request_en = MockRequest(headers={"Accept-Language": "en-US,en;q=0.9"})
    mock_request_sw = MockRequest(headers={"Accept-Language": "sw-KE,sw;q=0.9"})
    mock_request_fr = MockRequest(headers={"Accept-Language": "fr-FR,fr;q=0.9"})
    mock_request_unsupported = MockRequest(headers={"Accept-Language": "de-DE,de;q=0.9"})
    mock_request_no_header = MockRequest(headers={})

    print(f"Locale from EN request: {get_locale_from_request(mock_request_en)}")
    print(f"Locale from SW request: {get_locale_from_request(mock_request_sw)}")
    print(f"Locale from FR request: {get_locale_from_request(mock_request_fr)}")
    print(f"Locale from unsupported request: {get_locale_from_request(mock_request_unsupported)}")
    print(f"Locale from no header request: {get_locale_from_request(mock_request_no_header)}")

    # Restore original config
    config = original_config
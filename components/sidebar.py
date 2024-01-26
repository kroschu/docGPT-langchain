import asyncio
import os

import streamlit as st

from docGPT import GPT4Free


def side_bar() -> None:
    with st.sidebar:
        with st.expander(':orange[How to use?]'):
            st.markdown(
                """
              1. Введіть ваші ключі API: (Ви можете використовувати безкоштовну модель `gpt4free` **без ключів API**)
                                    * `OpenAI API Key`: Переконайтеся, що у вас ще залишився термін використання
                                    * `SERPAPI API Key`: Необов'язково. Якщо ви хочете задати питання про вміст, який не з'являється в PDF-документі, вам знадобиться цей ключ.
                                2. Завантажте файл **Документ** (виберіть один спосіб):
                                    * спосіб 1: Знайдіть і завантажте власний файл документа з вашого локального комп'ютера.
                                    * Спосіб 2: Введіть URL-адресу документа безпосередньо.
                                    
                                    (**допоміжні документи**: `.pdf`, `.docx`, `.csv`, `.txt`)
                                3. Почніть задавати питання!
                                4. Більше деталей (https://github.com/Lin-jun-xiang/docGPT-streamlit)
                                5. Якщо у вас виникли запитання, не соромтеся залишати коментарі та брати участь у дискусіях.(https://github.com/Lin-jun-xiang/docGPT-streamlit/issues
                """
            )

    with st.sidebar:
        if st.session_state.openai_api_key:
            OPENAI_API_KEY = st.session_state.openai_api_key
            st.sidebar.success('API key loaded form previous input')
        else:
            OPENAI_API_KEY = st.sidebar.text_input(
                label='#### Твій OpenAI API ключ 👇',
                placeholder="sk-...",
                type="password",
                key='OPENAI_API_KEY'
            )
            st.session_state.openai_api_key = OPENAI_API_KEY

        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    with st.sidebar:
        if st.session_state.serpapi_api_key:
            SERPAPI_API_KEY = st.session_state.serpapi_api_key
            st.sidebar.success('API key loaded form previous input')
        else:
            SERPAPI_API_KEY = st.sidebar.text_input(
                label='#### Твій SERPAPI API ключ 👇',
                placeholder="...",
                type="password",
                key='SERPAPI_API_KEY'
            )
            st.session_state.serpapi_api_key = SERPAPI_API_KEY

        os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY

    with st.sidebar:
        gpt4free = GPT4Free()
        st.session_state.g4f_provider = st.selectbox(
            (
                "#### Виберіть провайдера, якщо хочете користуватися безкоштовною моделлю. "
                "([Докладно](https://github.com/xtekky/gpt4free#models))"
            ),
            (['BestProvider'] + list(gpt4free.providers_table.keys()))
        )

        st.session_state.button_clicked = st.button(
            'Show Available Providers',
            help='Click to test which providers are currently available.',
            type='primary'
        )
        if st.session_state.button_clicked:
            available_providers = asyncio.run(gpt4free.show_available_providers())
            st.session_state.query.append('What are the available providers right now?')
            st.session_state.response.append(
                'The current available providers are:\n'
                f'{available_providers}'
            )

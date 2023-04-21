invalid_data_for_username_and_email_fields = [
    (
        {
            'email': ('a' * 244) + '@exeample.com',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `email`: его содержимое не должно быть '
            'длиннее 254 символа.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'username': ('a' * 151)
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `username`: его содержимое не должно быть '
            'длиннее 150 символов.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'username': '|-|aTa|_|_|a'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `username` проверяется на соответствие '
            'паттерну, указанному в спецификации: ^[\\w.@+-]+\\z'
        ),)
    )
]

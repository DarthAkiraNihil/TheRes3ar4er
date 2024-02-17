import os

config = {
    'r34api': {
        'template': 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index',
        'limit_per_request': 30
    },

    'bot': {
        'token': os.environ['THE_R34ER_TOKEN'],
        'prefix': '$r34er-',
        'daily_dose_chan': os.environ['DOSE_CHANNEL'],
        'sandbox_chan': os.environ['SANDBOX_CHANNEL'],
        'report_chan': os.environ['REPORT_CHANNEL'],
        'sending_delay': 1,
        'locale': 'ru'
    },
    'log_dumper': {
        'token': os.environ['LOG_DUMPER_TOKEN'],#os.environ['LOG_DUMPER_TOKEN'],
        'chat_id': os.environ['CHAT_ID']
    }
}
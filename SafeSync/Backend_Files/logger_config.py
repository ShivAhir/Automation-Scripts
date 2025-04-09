import logging

# to log if something goes wrong while we run the app
logging.basicConfig(
    filename='app.log',  
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


logger = logging.getLogger(__name__)
from app import app

application = app #aws looks for application variable
    
if __name__=='__main__':
    application.run()
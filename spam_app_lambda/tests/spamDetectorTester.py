import requests
import pandas as pd
import time
import json

class SpamDetectorTester:
    '''
    Tests the spam detector with different cases
    main runs all_tests
        all_tests run every type of test like spam emails, phishing emails elc
        each test tests each email by running test_single_email and prints the result
    then a summary is created of all the tests and how accurate they were'''
    def __init__(self, url: str = "http://127.0.0.1:5001"):
        self.url = url 
        self.api_url = f"{url}/predict_api"
        self.results = []
    
    def test_single_email(self, subject:str, message:str,expected:str)-> dict:
        '''Tests a single email'''
        email = { 'subject':subject, 
                 'message':message
                 }
               
        #time how long it takes
        start_time = time.time()

        try:
            response = requests.post(self.api_url, json=email)#sends email to app.py and process it, then sends prediction, and percentages
            response_time = time.time() - start_time

            if response.status_code == 200: #went through
                result = response.json()

                #check if there is an error
                if 'error' in result:                                                                   
                    error_result = {
                        'status': 'error',
                        'error': result['error'],
                        'response time': response_time,
                        'expected': expected,
                        'email subject': subject[:50] + "..." if len(subject) > 50 else subject
                        } 
                    self.results.append(error_result)    
                    return error_result   
                
                #return a result dict with info about connection
                result['response time'] = response_time
                result['status'] = 'success'
                result['expected prediction'] = expected
                result['email subject'] = subject[:50] if len(subject) > 50 else subject
                #does expected match pred
                if expected: #if there is an expected label
                    result['correctly_predicted'] = result.get('Prediction','') == expected #1 if they match 0 otherwise
                #get confidence as the higher of the two probabilities
                confidence = max(result['Spam probability'],result['Ham probability'])
                result['confidence'] = round(confidence,2)

                self.results.append(result)
                return result
        
            else:
                error_result = {
                    'status': 'error',
                    'error': f"HTTP:{response.status_code}",
                    'response_time': response_time,
                    'expected': expected,
                    'test_subject': subject[:50] + "..." if len(subject) > 50 else subject
                }
                self.results.append(error_result)
                return error_result
        except Exception as e:
            error_result = {
                    'status': 'error',
                    'error': str(e),
                    'response_time': time.time() - start_time,
                    'expected': expected,
                    'test_subject': subject[:50] + "..." if len(subject) > 50 else subject
            }
            self.results.append(error_result)
            
            return error_result
        
    def run_all_tests(self)-> dict:
        '''Runs all the tests'''
        print('Starting Testing')
        print('='*60)

        #clear previous results
        self.results =[] 
        self.test_obvious_spam()
        
        self.test_obvious_ham()
        self.test_phishing_attempts()
        self.test_marketing_emails()
        self.test_personal_emails()
        self.test_edge_cases()
        self.test_error_conditions()
        
        #print summary
        self.generate_summary()



    def test_obvious_spam(self):
        """Test obvious spam emails"""
        print("\nTesting Obvious Spam Emails...")
        
        spam_tests = [
            {
                'subject': "URGENT: You've Won $1,000,000!!!",
                'message': "Congratulations! You have been selected as our GRAND PRIZE WINNER! Click here NOW to claim your $1,000,000 prize! Limited time offer - expires in 24 hours!",
                'expected': 'Spam'
            },
            {
                'subject': "Make $5000 per week working from home!",
                'message': "Amazing opportunity! Work from home and make $5000+ per week! No experience needed! Free training provided! Click here to start making money today!",
                'expected': 'Spam'
            },
            {
                'subject': "FREE PILLS! VIAGRA! NO PRESCRIPTION NEEDED!",
                'message': "Get FREE pills delivered to your door! No prescription needed! VIAGRA, CIALIS and more! Order now and save 90%! Click here!",
                'expected': 'Spam'
            },
            {
                'subject': "Your account will be suspended",
                'message': "Your account has suspicious activity. Click this link immediately to verify your identity or your account will be permanently suspended within 24 hours!",
                'expected': 'Spam'
            }
        ]
            
        for test in spam_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)
    
    def test_obvious_ham(self):
        """Test obvious legitimate emails"""
        print('='*60)
        print("\nTesting Obvious Ham Emails...")
        
        ham_tests = [
            {
                'subject': "Meeting tomorrow at 3pm",
                'message': "Hi, just confirming our project meeting scheduled for tomorrow at 3pm in conference room B. I'll bring the quarterly reports we discussed.",
                'expected': 'Not Spam'
            },
            {
                'subject': "Weekend plans",
                'message': "Hey! Are we still on for dinner this Saturday? I made reservations at that new Italian place downtown for 7pm. Let me know if that works.",
                'expected': 'Not Spam'
            },
            {
                'subject': "Project update",
                'message': "The Q3 project is progressing well. We've completed 80% of the development phase and are on track for the October deadline. Next sprint starts Monday.",
                'expected': 'Not Spam'
            },
            {
                'subject': "Thank you for your order",
                'message': "Thank you for your recent purchase. Your order #12345 has been shipped and should arrive within 3-5 business days. Tracking information is attached.",
                'expected': 'Not Spam'
            }
        ]
        
        for test in ham_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)
        
    def test_phishing_attempts(self):
        """Test phishing and scam emails"""
        print("\nTesting Phishing Attempts...")
        
        phishing_tests = [
            {
                'subject': "PayPal: Verify your account immediately",
                'message': "We've detected unusual activity on your PayPal account. Click here to verify your identity immediately or your account will be limited.",
                'expected': 'Spam'
            },
            {
                'subject': "IRS: Tax refund pending",
                'message': "You have a tax refund of $2,847 pending. Click here to provide your banking information to receive your refund immediately.",
                'expected': 'Spam'
            },
            {
                'subject': "Amazon: Suspicious login detected",
                'message': "Someone tried to access your Amazon account from an unknown device. Click here to secure your account and change your password.",
                'expected': 'Spam'
            }
        ]
        
        for test in phishing_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)
    
    def test_marketing_emails(self):
        """Test marketing/promotional emails"""
        print('='*60)
        print("\nTesting Marketing Emails")
        
        marketing_tests = [
            {
                'subject': "Weekly Newsletter - Tech Updates",
                'message': "Here are this week's top technology stories: Apple announces new MacBook Pro, Google updates search algorithm, Microsoft releases security patches.",
                'expected': 'Ham'
            },
            {
                'subject': "Sale: 50% off everything",
                'message': "Our biggest sale of the year is here! Get 50% off all items with code SAVE50. Valid through Sunday. Shop now and save big!",
                'expected': None  # Could be either
            }
        ]
        
        for test in marketing_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)
    
    def test_personal_emails(self):
        """Test personal communication"""
        print("\nTesting Personal Emails...")
        
        personal_tests = [
            {
                'subject': "Happy Birthday!",
                'message': "Hope you have a wonderful birthday! Let's celebrate this weekend. I'll call you later to make plans.",
                'expected': 'Ham'
            },
            {
                'subject': "Re: Vacation photos",
                'message': "Thanks for sharing the vacation photos! They look amazing. That sunset shot is my favorite. When are you planning your next trip?",
                'expected': 'Ham'
            }
        ]
        
        for test in personal_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)
    
    def test_error_conditions(self):
        """Test error handling"""
        print("\nTesting Error Conditions...")
        
        # Test completely empty request
        try:
            response = requests.post(self.api_url, json={})
            print(f"Empty request: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Empty request error: {e}")
        
        # Test malformed JSON
        try:
            response = requests.post(self.api_url, data="invalid json", 
                                   headers={'Content-Type': 'application/json'})
            print(f"Invalid JSON: {response.status_code}")
        except Exception as e:
            print(f"Invalid JSON error: {e}")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print('='*60)
        print("\nTesting Edge Cases...")
        
        edge_tests = [
            {
                'subject': "",
                'message': "Quick question about the presentation",
                'expected': None  # Don't know expected result
            },
            {
                'subject': "Meeting",
                'message': "",
                'expected': None
            },
            {
                'subject': "Special offer just for you",
                'message': "We noticed you browsed our website recently. Here's a 20% discount on your next purchase. Use code SAVE20 at checkout.",
                'expected': None  # Could go either way
            },
            {
                'subject': "A" * 200,  # Very long subject
                'message': "This is a test with a very long subject line to see how the classifier handles it.",
                'expected': None
            },
            {
                'subject': "Test",
                'message': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50,  # Very long message
                'expected': None
            }
        ]
        
        for test in edge_tests:
            result = self.test_single_email(test['subject'], test['message'], test['expected'])
            self.print_results(result)

    def print_results(self, result: dict):
        '''Prints all test results'''
        #get successful tests
        
        if result['status'] == 'success':
            prediction = result.get('Prediction','N/A')
            confidence = result.get('confidence','N/A')
            subject = result.get('email subject','N/A')

            #if there is a prediction
            if result.get('expected prediction'): 
                if result.get('correctly_predicted'):
                    print(f"For email with subject {subject}  \n{prediction} is the correct prediction ✅ with {confidence}% confidence in {result['response time']:.4f}s")
                else:
                    print(f"For email with subject {subject} \n{prediction} is the wrong prediction ❌ with {confidence}% confidence in {result['response time']:.4f}s (Expected: {result['expected prediction']})")
            #there is no expected prediction given in the test data
            else:
                print(f"For email with subject {subject}\nThe prediction is: {prediction} with {confidence}% confidence in {result['response time']:.2f}s")

        else:
            subject = result.get('email subject','N/A')
            print(f"For email with subject: {subject}, there is an error\nThe error is:{result['error']}")
            


    def generate_summary(self, save_summary=False)-> dict:
        '''Generates a summary report of all the tests'''
        print("="*60)
        print("\nGenerating Summary Report...")

        #metric calculations
        total_tests = len(self.results)
        successful_tests= len([r for r in self.results if r['status']=='success'])
        failed_tests = total_tests - successful_tests
        tests_with_label = [r for r in self.results if r.get('status') == 'success' and r.get('expected prediction')]
        correct_predictions = len([r for r in self.results if r.get('correctly_predicted')])
        
        summary = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'failed_tests': failed_tests,
            'accuracy': correct_predictions/len(tests_with_label) if tests_with_label else None,

        }
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        
        if summary['accuracy'] is not None:
            print(f"Accuracy: {summary['accuracy']:.2%} ->({correct_predictions}/{len(tests_with_label)})")
       
        print(summary)

    def save_resutlts(self):
        results_df = pd.DataFrame(self.results)
        col_order = ['email subject','status','expected prediction','Prediction','correctly_predicted', 'Ham probability', 'Spam probability','confidence', 'response time', 'error']
        results_df=results_df[col_order]
        results_df.to_csv('results_dataframe.csv', index=False)
        print(results_df)

def main():
    
    tester = SpamDetectorTester()

    #check if API is available
    print(f'Testing {tester.api_url}')
    
    try:
       
       response = requests.get(tester.api_url, timeout=5)      
       print('Status code= ', response.status_code)
       print(f"Flask app is running at{tester.api_url}")
    except:
        print('Flask app is not available, make sure to run app.py')
        return
   
    tester.run_all_tests()  
    tester.generate_summary()
    tester.save_resutlts()


if __name__ == "__main__":
    main()
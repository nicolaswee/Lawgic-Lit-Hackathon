# -*- coding: utf-8 -*-

import json
import requests
import time
import urllib
import telegram
from random import shuffle
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler


TOKEN = "BOT API KEY HERE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(token=TOKEN)

#To grab category
def getCategory():
    with open('data.json') as f:
        data = json.load(f)
    return data.keys()

#Get Lawyer by Category
def getLawyersByCat(search):
    with open('data.json') as f:
        data = json.load(f)
    
    if search in data.keys():
        rlist = data[search]
        shuffle(rlist)
        size = 10
        if len(rlist) < size:
            size = len(rlist)
        
        results = { i : rlist[i] for i in range(0, size) }    

    list_of_lawyers = ''
    for lawyer in results.values():
        list_of_lawyers += lawyer.replace('\"', '').title() + '\n'
    return list_of_lawyers
""" 
Download content from URL
Return string
"""
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

"""
Get string from json
"""
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

"""
Get messages sent to bot
"""
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js
    
    
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
    

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    print("===================")
    print(updates)
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def start(bot, update):
    kb = [[InlineKeyboardButton("Criminal Law", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Legal Contracts", callback_data="Legal Contracts")]]

    reply_markup = InlineKeyboardMarkup(kb)
    update.message.reply_text("Which area of law does your case fall under?", reply_markup=reply_markup)

def kbCallback(bot, update):
    query = update.callback_query
    text = query.data
    chat_id = query.message.chat_id

    print(text)
    if text == "/start":
        kb = [[InlineKeyboardButton("Criminal Law", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Legal Contracts", callback_data="Legal Contracts")]]


        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Which area of law does your case fall under?", reply_markup=reply_markup)

#Legal Contracts
    if text == "Legal Contracts":
        kb = [[InlineKeyboardButton("Business Contract Issues", callback_data="Business Contract Issues")],
        [InlineKeyboardButton("Common Contractual Issues", callback_data="Common Contractual Issues")],
        [InlineKeyboardButton("Back", callback_data="/start")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="You have selected Legal Contracts", reply_markup=reply_markup)

#Business Contract Issues
    if text == "Business Contract Issues":
        kb = [[InlineKeyboardButton("Shareholder Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Partnership Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Non-Disclosure Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Employment Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Distributor Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Tenancy Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Consultancy Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Freelance Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Service Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Business Referral Agreements in Singapore", callback_data="FYI")],
        [InlineKeyboardButton("Back", callback_data="Legal Contracts")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Please selected the Business Contract Issue you are interested in.", reply_markup=reply_markup)

#Common Contractual Issues
    if text == "Common Contractual Issues":
        kb = [[InlineKeyboardButton("Contracting via Electronic Communications", callback_data="FYI")],
        [InlineKeyboardButton("Can I compel another party to honour an agreement?", callback_data="FYI")],
        [InlineKeyboardButton("Punitive Damages in Singapore Contract Law", callback_data="FYI")],
        [InlineKeyboardButton("Entire Agreement Clauses in Singapore: What are They and What Do They Do?", callback_data="FYI")],
        [InlineKeyboardButton("Assignment and Novation: How to Transfer a Contract in Singapore", callback_data="FYI")],
        [InlineKeyboardButton('Implied Terms: Filling in "Gaps" in a Contract', callback_data='FYI')],
        [InlineKeyboardButton("6 Issues to Consider Before Agreeing to Be a Loan Guarantor", callback_data="FYI")],
        [InlineKeyboardButton("Guide to Indemnity Clauses in Singapore Commercial Contracts", callback_data="FYI")],
        [InlineKeyboardButton("What is the governing law of a contract?", callback_data="FYI")],
        [InlineKeyboardButton("Breach of Contract in Singapore", callback_data="Breach of Contract in Singapore")],
        [InlineKeyboardButton("Back", callback_data="Legal Contracts")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Please selected the Common Contractual Issue you are interested in.", reply_markup=reply_markup)

#FYI
    if text == "FYI":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="/start")]]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="For your Information: https://singaporelegaladvice.com/law-articles/legal-contracts", reply_markup=reply_markup)

#Breach of Contract in Singapore
    if text == "Breach of Contract in Singapore":
        kb = [[InlineKeyboardButton("What are the Remedies Available for Breach of Contract?", callback_data="What are the Remedies Available for Breach of Contract?")],
        [InlineKeyboardButton("What is Breach of Contract?", callback_data="What is Breach of Contract?")],
        [InlineKeyboardButton('What Constitutes "Failure"?', callback_data='What constitutes "failure"?')],
        [InlineKeyboardButton("What is a Breach of Contract Dispute?", callback_data="FYA")],
        [InlineKeyboardButton("Back", callback_data="Legal Contracts")]]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="You have selected Breach of Contract in Singapore", reply_markup=reply_markup)

#What are the Remedies Available for Breach of Contract?
    if text == "What are the Remedies Available for Breach of Contract?":
        kb = [[InlineKeyboardButton("Damages", callback_data="Damages")],
        [InlineKeyboardButton("Specific Performance", callback_data="Specific Performance")],
        [InlineKeyboardButton('Terminate Contract', callback_data='Terminate Contract')],
        [InlineKeyboardButton("Prohibitory injunction", callback_data="Prohibitory injunction")],
        [InlineKeyboardButton("Back", callback_data="Breach of Contract in Singapore")]]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="These are the Remedies Available for Breach of Contract.", reply_markup=reply_markup)

#Damages
    if text == "Damages":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="What are the Remedies Available for Breach of Contract?")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="The principal remedy for breach of contract is monetary compensation, also known as damages in legal parlance. By default, every breach of contract entitles the innocent party to damages for losses suffered by the innocent party stemming from the breach of contract. The innocent party must, however, take reasonable steps to miminise his losses.", reply_markup=reply_markup)

#Specific Performance
    if text == "Specific Performance":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="What are the Remedies Available for Breach of Contract?")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="An order of specific performance may be available to compel the defaulting party to perform his contractual obligation. However, specific performance is only awarded in exceptional cases, typically where damages are an inadequate remedy should the contractual obligation not be performed. For example, specific performance is more likely to be available in contracts involving the delivery of unique property, such as land.", reply_markup=reply_markup)

#Terminate Contract
    if text == "Terminate Contract":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="What are the Remedies Available for Breach of Contract?")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="A breach of contract may entitle the innocent party to terminate the contract. If the innocent party chooses to terminate the contract, the contracting parties are discharged from all contractual obligations as at the point of termination onwards. Unlike damages, not every breach of contract entitles the innocent party to terminate the contract. Whether or not the right of termination is available depends on how the term is classified in law.", reply_markup=reply_markup)

#Prohibitory injunction
    if text == "Prohibitory injunction":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="What are the Remedies Available for Breach of Contract?")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="A prohibitory injunction may be available to ensure that the defaulting party honours his promise not to do something. Like specific performance, prohibitory injunctions are only awarded in exceptional cases, typically where damages are inadequate to remedy the breach of contract.", reply_markup=reply_markup)

#What is Breach of Contract?
    if text == "What is Breach of Contract?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="Breach of Contract in Singapore")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Assuming that a valid and legally binding contract exists, a breach of contract occurs when a contracting party (the “defaulting party”) fails to perform, without lawful excuse, a contractual obligation.", reply_markup=reply_markup)

#What constitutes "failure"?
    if text == 'What constitutes "failure"?':
        kb = [[InlineKeyboardButton("Criteria for failure of performance", callback_data="Criteria for failure of performance")],
        [InlineKeyboardButton("Categories of failure of performance", callback_data="Categories of failure of performance")],
        [InlineKeyboardButton("Back", callback_data="Breach of Contract in Singapore")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="These constitutes 'Failure'.", reply_markup=reply_markup)

#Criteria for failure of performance 
    if text == 'Criteria for failure of performance':
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="Breach of Contract in Singapore")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="However, not every failure to perform constitutes “breach of contract”. Two other elements must be satisfied for a failure to perform to constitute “breach of contract”: 1. the defaulting party must have failed to perform a contractual obligation. 2. there must be no lawful excuse for the defaulting party’s failure to perform. Such excuse must be provided for either in the contract, or by law.", reply_markup=reply_markup)

#Categories of failure of performance
    if text == 'Categories of failure of performance':
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Legal Contracts")],
        [InlineKeyboardButton("Back", callback_data="Breach of Contract in Singapore")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Non-performance (i.e. when a defaulting party refuses to perform what he has promised to do); Defective performance (i.e. the defaulting party fails to fulfil a promised objective or end-state) Doing the very thing the defaulting party has promised not to do; and Preventing oneself from fulfilling a contractual obligation.", reply_markup=reply_markup)

#Categories of failure of performance
    if text == 'FYA':
        kb = [[InlineKeyboardButton("Court Proceedings", callback_data="Court proceedings")],
        [InlineKeyboardButton("Private Mediation", callback_data="Private Mediation")],
        [InlineKeyboardButton("Small Claims Tribunals", callback_data="Small Claims Tribunals")],
        [InlineKeyboardButton("Employee Disputes under Employment Act", callback_data="Employee Disputes for employees under Employment Act")],
        # [InlineKeyboardButton("Employment contracts disputes for employees under the Employment Act", callback_data="Employment contracts disputes for employees under the Employment Act")],
        [InlineKeyboardButton("Back", callback_data='Breach of Contract in Singapore')]]
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Assuming that a valid and legally binding contract exists, a breach of contract occurs when a contracting party (the “defaulting party”) fails to perform, without lawful excuse, a contractual obligation.", reply_markup=reply_markup)


#Where can I go to resolve a breach of contract dispute?
    if text == "FYB":
        kb = [[InlineKeyboardButton("Court proceedings", callback_data="Court proceedings")],
        [InlineKeyboardButton("Private Mediation", callback_data="Private Mediation")],
        [InlineKeyboardButton("Small Claims Tribunals", callback_data="Small Claims Tribunals")],
        [InlineKeyboardButton("Employee Disputes under Employment Act", callback_data="Employee Disputes for employees under Employment Act")],
        [InlineKeyboardButton("Back", callback_data='Breach of Contract in Singapore')],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Assuming that a valid and legally binding contract exists, a breach of contract occurs when a contracting party (the “defaulting party”) fails to perform, without lawful excuse, a contractual obligation.", reply_markup=reply_markup)


#Court proceedings
    if text == 'Court proceedings':
        kb = [[InlineKeyboardButton("Contact a Lawyer Now", callback_data="Court Proceedings Lawyer")],
        [InlineKeyboardButton("Back", callback_data="FYA")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="If a more formal mode of dispute resolution is preferred, Court proceedings or arbitration may be considered. Because of the level of formality involved, these tend to be more expensive and lengthy.", reply_markup=reply_markup)


#Private Mediation
    if text == 'Private Mediation':
        kb = [[InlineKeyboardButton("Contact a Lawyer Now", callback_data="Private Mediation Lawyer")],
        [InlineKeyboardButton("Back", callback_data="FYA")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="An alternative mode of dispute resolution is private mediation. Private mediation is less adversarial in nature because it focuses on arriving at an outcome that is most favourable to the interests of all parties concerned.", reply_markup=reply_markup)

#Small Claims Tribunals
    if text == 'Small Claims Tribunals':
        kb = [[InlineKeyboardButton("Contact a Lawyer Now", callback_data="Small Claims Tribunals Lawyer")],
        [InlineKeyboardButton("Back", callback_data="FYA")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="The Small Claims Tribunals deals with claims up to $10,000 (or $20,000 with the parties’ consent). It is a relatively quicker, cheaper and less formal forum for dispute resolution. Parties cannot be represented by lawyers at the Small Claims Tribunals.", reply_markup=reply_markup)

#Employment contracts disputes for employees under the Employment Act
    if text == 'Employee Disputes for employees under Employment Act':
        kb = [[InlineKeyboardButton("Wait for Ministry of Manpower or you can Contact a Lawyer Now", callback_data="Disputes Lawyer")],
        [InlineKeyboardButton("Back", callback_data="FYA")]]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="You have selected Employee Disputes for employees under Employment Act.", reply_markup=reply_markup)


#Court Proceedings Lawyer
    if text == 'Court Proceedings Lawyer' or text == 'Private Mediation Lawyer' or text == 'Small Claims Tribunals Lawyer' or text == 'Disputes Lawyer' :
        kb = [[InlineKeyboardButton("Click here for more Information", callback_data="FYC")],
        [InlineKeyboardButton("Back", callback_data="FYA")]]
        print(getLawyersByCat("contract"))
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text=getLawyersByCat("contract"), reply_markup=reply_markup)




































#Criminal Law
    if text == "Criminal Law":
        kb = [[InlineKeyboardButton("Sexual Offences", callback_data="Sexual Offences")], 
        [InlineKeyboardButton("Vice-Related Offences", callback_data="Vice-Related Offences")], 
        [InlineKeyboardButton("Cybercrime", callback_data="Cybercrime")], 
        [InlineKeyboardButton("White-Collar Crimes", callback_data="White-Collar Crimes")],
        [InlineKeyboardButton("Other Criminal Offences", callback_data="Other Criminal Offences")],
        [InlineKeyboardButton("Back", callback_data="/start")],]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Which Criminal Law category does your case fall under?", reply_markup=reply_markup)

#Sexual Offences\
    if text == "Sexual Offences":
        kb = [[InlineKeyboardButton("Legal Age for Sex in Singapore", callback_data="Legal Age for Sex in Singapore")], 
        [InlineKeyboardButton("Rape", callback_data="Rape")], 
        [InlineKeyboardButton('"Rape" of same gender (Sexual assault by Penetration)', callback_data='"Rape" of same gender (Sexual assault by Penetration)')], 
        [InlineKeyboardButton("Molest (Outrage of Modesty)", callback_data="Molest (Outrage of Modesty)")],
        [InlineKeyboardButton("Sexual Grooming", callback_data="Sexual Grooming")],
        [InlineKeyboardButton("Commercial Sex (Prostitution) with Minors", callback_data="Commercial Sex (Prostitution) with Minors")],
        [InlineKeyboardButton("Sexting", callback_data="Sexting")],
        [InlineKeyboardButton("Other Sexual Offences", callback_data="Other Sexual Offences")],
        [InlineKeyboardButton("Punishment", callback_data="Punishment")],
        [InlineKeyboardButton("Back", callback_data="Criminal Law")],
        ]

        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Which subject do you want to find out more about?", reply_markup=reply_markup)
        
        # keyboard1 = telegram.KeyboardButton(text="Legal Age for Sex in Singapore")
        # keyboard2 = telegram.KeyboardButton(text="Rape")
        # keyboard3 = telegram.KeyboardButton(text='"Rape" of same gender (Sexual assault by Penetration)')
        # keyboard4 = telegram.KeyboardButton(text="Molest (Outrage of Modesty)")
        # keyboard5 = telegram.KeyboardButton(text="Sexual Grooming")
        # keyboard6 = telegram.KeyboardButton(text="Commercial Sex (Prostitution) with Minors")
        # keyboard7 = telegram.KeyboardButton(text="Sexting")
        # keyboard8 = telegram.KeyboardButton(text="Other Sexual Offences")
        # keyboard9 = telegram.KeyboardButton(text="Punishment")
        # keyboard10 = telegram.KeyboardButton(text="/start")

        # custom_keyboard = [[keyboard1, keyboard2, keyboard3, keyboard4, keyboard5, keyboard6, keyboard7, keyboard8, keyboard9,keyboard10]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        # bot.send_message(chat_id=chat_id, text="Which subject do you want to find out more about?", reply_markup=reply_markup)

#Legal Age for Sex in Singapore
    if text == "Legal Age for Sex in Singapore":
        kb = [[InlineKeyboardButton("I didn't know that he/she was a minor.", callback_data="I didn't know that he/she was a minor.")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="The legal age to have sex in Singapore is 16 years old. This means that it is a punishable offence to have sex (whether vaginal, oral or anal) with persons below 16 years old, as stated in section 376A of the Singapore Penal Code.", reply_markup=reply_markup)


#I didn't know that he/she was a minor.
    if text == "I didn't know that he/she was a minor.":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Legal Age for Sex in Singapore")]]
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Section 377D of the Penal Code states that: Offenders above 21 years old cannot claim that they mistakenly believed the person was not underage as a defence. Offenders below 21 years old may claim that they mistakenly believed the person was not underage as a defence. However, this is only if that person is of the opposite sex, and if the offender has not committed any similar sexual offences before.", reply_markup=reply_markup)

#Rape
    if text == "Rape":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Sexual Offences")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under section 375 of the Penal Code, a man will be guilty of rape if he has vaginal sex with: Any woman without her consent; or A girl under 14 years old, regardless of whether she had given her consent.", reply_markup=reply_markup)

#"Rape" of same gender (Sexual assault by Penetration)
    if text == '"Rape" of same gender (Sexual assault by Penetration)':
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
    [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Women cannot technically commit “rape” as the rape provision (i.e. section 375 of the Penal Code) applies only to male offenders. However, they can be convicted for sexual assault by penetration under section 376 of the Penal Code if they use a part of their body (or an object) to penetrate another person’s vagina or anus without that person’s consent. Men also cannot technically “rape” male victims as the rape provision applies only to female victims. However, they can similarly be convicted of sexual assault by penetration if they have oral or anal sex with another male without his consent.", reply_markup=reply_markup)

#Molest (Outrage of Modesty)
    if text == "Molest (Outrage of Modesty)":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Molest is prosecuted as the offence of outrage of modesty in Singapore when it involves criminal force, pursuant to section 354 of the Penal Code.", reply_markup=reply_markup)

#Sexual Grooming
    if text == "Sexual Grooming":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Sexual grooming occurs when an offender on or above 21 years old meets another person under 16 years old with the intention of having sex, where the offender had previously met or communicated with him/her at least 2 times.", reply_markup=reply_markup)

#Commercial Sex (Prostitution) with Minors
    if text == "Commercial Sex (Prostitution) with Minors":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Commercial sex (i.e. paying for sex) with persons under 18 years old is a punishable offence under section 376B of the Penal Code. Under section 376C of the Penal Code, Singapore citizens or Permanent Residents who engage in commercial sex with persons under 18 will still be liable even if the acts were done outside of Singapore.", reply_markup=reply_markup)

#Sexting
    if text == "Sexting":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Sending sexually suggestive messages to a person under 16 year old may result in a prosecution under section 7 of the Children and Young Persons Act or section 76E of the Penal Code.", reply_markup=reply_markup)

#Other Sexual Offences
    if text == "Other Sexual Offences":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="Intercourse between men Incest, i.e. sex with family members Necrophilia, i.e. sex with corpses Bestiality, i.e. sex with animals Child prostitution Child pornography Sexual harassment (refer to Protection of Harassment Act) For more information: https://singaporelegaladvice.com/law-articles/sexual-harassment-in-singapore-workplace-sexual-harassment/", reply_markup=reply_markup)

#Punishment
    if text == "Punishment":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="The quantum of punishment for each respective sexual offence, such as the length of imprisonment or sum of fine, can be found in the Penal Code under the relevant sections for each offence.", reply_markup=reply_markup)

#Vice-Related Offences
    if text == "Vice-Related Offences":
        kb = [[InlineKeyboardButton("Prostitution", callback_data="Prostitution")],  
        [InlineKeyboardButton("Pornography", callback_data="Pornography")], 
        [InlineKeyboardButton("Drugs", callback_data="Drugs")], 
        [InlineKeyboardButton("Drinking Alcohol", callback_data="Drinking Alcohol")], 
        [InlineKeyboardButton("Gambling", callback_data="Gambling")], 
        [InlineKeyboardButton("Vaping", callback_data="Vaping")], 
        [InlineKeyboardButton("Drink Driving", callback_data="Drink Driving")], 
        [InlineKeyboardButton("Back", callback_data="Sexual Offences")]]
         
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Prostitution")
        # keyboard2 = telegram.KeyboardButton(text="Pornography")
        # keyboard3 = telegram.KeyboardButton(text='Drugs')
        # keyboard4 = telegram.KeyboardButton(text='Drinking Alcohol')
        # keyboard5 = telegram.KeyboardButton(text='Gambling')
        # keyboard6 = telegram.KeyboardButton(text='Vaping')
        # keyboard7 = telegram.KeyboardButton(text='Drink Driving')

        # custom_keyboard = [[keyboard1, keyboard2, keyboard3, keyboard4, keyboard5, keyboard6, keyboard7]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Which Viced-Related Offence category does your case fall under?", reply_markup=reply_markup)

#Prostitution 
    if text == "Prostitution":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Vice-Related Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # kb = [[InlineKeyboardButton("Back to Start", callback_data="/start")], 
        # [InlineKeyboardButton("Back", callback_data="Vice-Related Offences")]]
        
        # reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="It is not illegal to be a prostitute in Singapore. It is not illegal to visit a prostitute. However, many activities related to prostitution are illegal. For example, persistent soliciting by prostitutes is prohibited under section 19 of the Miscellaneous Offences (Public Order and Nuisance) Act. Check out more information at: https://singaporelegaladvice.com/law-articles/is-it-illegal-to-visit-prostitutes-in-singapore/", reply_markup=reply_markup)

#Pornography 
    if text == "Pornography":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Vice-Related Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        bot.send_message(chat_id=chat_id, text="It is against the law to keep, distribute or sell pornographic materials. It is also against the law to keep, distribute or sell pornographic films. If you accidentally stumble upon a pornographic website, it is not illegal to view the pornographic content, as long as you do not download any such obscene files and store them within your computer", reply_markup=reply_markup)

#Drugs
    if text == "Drugs":

        kb = [[InlineKeyboardButton("Possession of Drugs", callback_data="Possession of Drugs")], 
        [InlineKeyboardButton("Possession of Drugs", callback_data="Possession of Drugs")],
        [InlineKeyboardButton("Consumption of Drugs", callback_data="Consumption of Drugs")],
        [InlineKeyboardButton("Trafficking of Drugs", callback_data="Trafficking of Drugs")],
        [InlineKeyboardButton("Back", callback_data="Vice-Related Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Possession of Drugs")
        # keyboard2 = telegram.KeyboardButton(text="Consumption of Drugs")
        # keyboard3 = telegram.KeyboardButton(text='Trafficking of Drugs')
        # keyboard4 = telegram.KeyboardButton(text="Vice-Related Offences")
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3,keyboard4]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="You have selected Drugs.", reply_markup=reply_markup)

#Possession of Drugs
    if text == "Possession of Drugs":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="It is an offence under section 8(a) of the MDA to possess controlled drugs. The penalty for possessing drugs is a maximum of 10 years’ imprisonment, or a fine of $20,000 or both.. <Presumption of drug possession>. For example, if the police finds a packet of special K at your house that your friend left behind after a party, under section 18 of the MDA you are presumed to possess that drug, and to have known that it was a prohibited drug, unless you can prove otherwise. It does not matter that you have never come into physical contact with the drug.", reply_markup=reply_markup)


#Consumption of Drugs
    if text == "Consumption of Drugs":
        kb = [[InlineKeyboardButton("Urine Tests and Hair Tests", callback_data="Urine Tests and Hair Tests")], 
        [InlineKeyboardButton("Presumption of Drug Consumption", callback_data="Presumption of Drug Consumption")], 
        [InlineKeyboardButton("Possession of Drug Consumption Apparatus", callback_data="Possession of Drug Consumption Apparatus")], 
        [InlineKeyboardButton("Consuming Drugs Overseas", callback_data="Consuming Drugs Overseas")], 
        [InlineKeyboardButton("Back", callback_data="Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Urine Tests and Hair Tests")
        # keyboard2 = telegram.KeyboardButton(text="Presumption of Drug Consumption")
        # keyboard3 = telegram.KeyboardButton(text='Possession of Drug Consumption Apparatus')
        # keyboard4 = telegram.KeyboardButton(text='Consuming Drugs Overseas')
        # keyboard5 = telegram.KeyboardButton(text='Drugs')
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3, keyboard4,keyboard5]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under section 8(b) of the MDA, consumption of any controlled drug or specified drug is an offence. (Specified drugs refer to certain controlled drugs that are listed separately in the Fourth Schedule.) The penalty for consuming either controlled or specified drugs is a maximum of 10 years’ imprisonment, or a fine of $20,000 or both. The general penalty for repeat drug consumption of a controlled drug is imprisonment of at least 3 years. However, in cases of specified drugs, you will be punished under section 33A if you have been previously: Admitted into an institution; Convicted for consuming a specified drug; and/or Convicted for an offence of failure to provide a urine specimen, and are convicted once again for consuming a specified drug or failing to provide a urine specimen, you will be punished with imprisonment for at least 5 to 7 years and receive 3 to 6 strokes of the cane.", reply_markup=reply_markup)


#Urine Tests and Hair Tests
    if text == "Urine Tests and Hair Tests":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Consumption of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Consumption of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="If the police have reason to believe that you have consumed drugs, they have the right to subject you to a urine test and/or a hair test under sections 31 and 31A of the MDA. Failure to provide a specimen of urine for a urine test, will result in a maximum of 10 years’ imprisonment, or a fine of $20,000 or both. Failure to provide specimens of your hair for a hair test is punishable with a maximum of 2 years’ imprisonment, or a fine of $5,000 or both.", reply_markup=reply_markup)

#Presumption of Drug Consumption
    if text == "Presumption of Drug Consumption":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Consumption of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Consumption of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under section 22 of the MDA, if a controlled drug is found in a person’s urine, he is presumed to have consumed the drug illegally under section 8(b) of the MDA. This is unless he can prove that the drug consumption was involuntary, which can be a difficult burden to discharge.", reply_markup=reply_markup)

#Possession of Drug Consumption Apparatus
    if text == "Possession of Drug Consumption Apparatus":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Consumption of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Consumption of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Possessing apparatus used for consuming controlled drugs, like pipes, syringes and other utensils can also land you in jail for a maximum of 3 years or a fine of $10,000 or both.", reply_markup=reply_markup)

#Consuming Drugs Overseas
    if text == "Consuming Drugs Overseas":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Consumption of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Consumption of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under section 8A of the MDA, a Singaporean or PR who consumes drugs abroad will be dealt with as if that offene had been committed within Singapore and punished accordingly . Note that random checks are conducted at Changi Airport and Woodlands.", reply_markup=reply_markup)

#Trafficking of Drugs
    if text == "Trafficking of Drugs":
        kb = [[InlineKeyboardButton("Presumption of Drug Possession for the Purpose of Trafficking", callback_data="Presumption of Drug Possession for the Purpose of Trafficking")], 
        [InlineKeyboardButton("Consumption of Drugs", callback_data="Consumption of Drugs")],
        [InlineKeyboardButton("Penalty for Drug Trafficking", callback_data="Penalty for Drug Trafficking")],
        [InlineKeyboardButton("Rehabilitation for Drug Addicts", callback_data="Rehabilitation for Drug Addicts")],
        [InlineKeyboardButton("Back", callback_data="Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Presumption of Drug Possession for the Purpose of Trafficking")
        # keyboard2 = telegram.KeyboardButton(text="Penalty for Drug Trafficking")
        # keyboard3 = telegram.KeyboardButton(text='Rehabilitation for Drug Addicts')
        # keyboard4 = telegram.KeyboardButton(text='Drugs')
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3,keyboard4]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The most serious of the trio is the offence of drug trafficking under section 5 of the MDA. If you are involved in selling, transporting, delivering, distributing or even offering to do any of these acts, you would be committing an offence. On the other hand, you can also be convicted if you order someone else to transport any controlled drug. This also applies to trafficking drugs on someone else’s behalf, regardless of whether that person is in Singapore. A point to note is that under the MDA, trafficking drugs and importing/exporting drugs are different, but both are offences under the Act.", reply_markup=reply_markup)

#Presumption of Drug Possession for the Purpose of Trafficking
    if text == "Presumption of Drug Possession for the Purpose of Trafficking":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Trafficking of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Trafficking of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="If the quantity of drugs in your possession exceeds a certain amount, as stipulated under section 17 of the MDA, you are presumed to possess the drugs for the purpose of trafficking.", reply_markup=reply_markup)

#Penalty for Drug Trafficking
    if text == "Penalty for Drug Trafficking":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Trafficking of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Trafficking of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Depending on the class and the quantity of the drugs trafficked, the penalty ranges from imprisonment and strokes of cane to the mandatory death penalty. However, with effect from 1 January 2013, convicted drug traffickers may be able to avoid the mandatory death penalty if they can prove that they were only couriers in charge of transporting, sending or delivering the drug. Additionally, it has to be shown that: They had either “substantively assisted” the Central Narcotics Bureau (the government agency in charge of drug enforcement in Singapore, also known as CNB) in disrupting drug trafficking activities within or outside Singapore; or They were suffering from a condition that substantially impaired their mental responsibility for their actions. In such circumstances, the drug trafficker may be sentenced to life imprisonment instead. If the drug trafficker managed to avoid the death penalty on the basis of only having “substantively assisted” CNB, he must also be caned up to 15 strokes. Currently, the extent of assistance the drug trafficker must have given in order for his efforts to be regarded as “substantive” is unclear, and is entirely at the Public Prosecutor’s discretion.", reply_markup=reply_markup)

#Rehabilitation for Drug Addicts
    if text == "Rehabilitation for Drug Addicts":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")], 
        [InlineKeyboardButton("Back", callback_data="Trafficking of Drugs")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Trafficking of Drugs")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="A drug addict is someone who has developed a desire or need to continue consuming drugs, or is dependent on the effects of drugs. If the Director of CNB suspects that you are a drug addict, you may be required to be medically examined and observed, or be subject to urine and/or hair testing. Through the results of the examination, you may be ordered to be admitted into a rehabilitation centre to undergo treatment and rehabilitation for 6 months (extendable up to 3 years) at the Drug Rehabilitation Centres (DRCs). This only applies if you are arrested solely for drug consumption. Such an order would be in imposed in lieu of a jail sentence for first and second-time drug abusers. After that, if you are arrested for drug consumption again, you will be tried in court and upon conviction, will face a long-term prison sentence. Youth drug addicts aged 16 to below 21, will be placed in a 6-month residence at the Community Rehabilitation Centre (CRC) upon being detained in the DRC.", reply_markup=reply_markup)


#Gambling
    if text == "Gambling":
        kb = [[InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Gambling can generally be classified into 3 categories: Gaming, which generally refers to games of chance and skill.  E.g. -- Dai Di”, the card game also known as Big Two. It is  illegal to game in public Lotteries such as 4D or the Singapore Sweep Betting, which can include wagering on football matches or horse races. However, the operation of gambling dens is illegal. Jackpot machines are also banned in Singapore, in accordance with the Private Lotteries Act, except when permission is granted or as in the case of legalised casinos.", reply_markup=reply_markup)

#Vaping
    if text == "Vaping":
        kb = [[InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under section 16(2A) of the Tobacco (Control of Advertisements and Sale) Act (TCASA), it is illegal to possess, purchase and use vaporisers in Singapore as of 1 February 2018. This includes e-cigarettes, e-pipes and e-cigars as the TCASA covers any toy, device or article: That resembles, or is designed to resemble, a tobacco product; That is capable of being smoked; That may be used in such a way as to mimic the act of smoking; or The packaging of which resembles, or is designed to resemble, the packaging commonly associated with tobacco products. Persons found guilty of this offence can be fined up to $2,000 Under section 16(1) of the TCASA, it has been illegal to import vaporisers from 1 August 2016 onwards. This means that buying vaporisers online and shipping them to Singapore for personal use is illegal. Those guilty of the offence are liable to a fine of up to $10,000 and/or up to 6 months’ jail. Repeat offenders are liable to a fine of up to $20,000 and/or to 12 months’ jail.", reply_markup=reply_markup)

#Drink Driving
    if text == "Drink Driving":
        kb = [[InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="You are guilty of drink driving under section 67 of the Road Traffic Act (RTA) if you: Are unfit to drive under the influence of alcohol to the extent you are incapable of having proper control of the vehicle; or Exceed the prescribed alcohol limit The prescribed alcohol limit is: 35 microgrammes of alcohol in 100 millilitres of breath; or 80 milligrammes of alcohol in 100 millilitres of blood Under section 69 of the RTA, police officers are empowered to ask for a specimen of your breath for a preliminary breath test. If you refuse to do so, police officers can arrest you without a warrant.", reply_markup=reply_markup)

#Drinking Alcohol
    if text == "Drinking Alcohol":
        kb = [[InlineKeyboardButton("Legal Drinking Age", callback_data="Legal Drinking Age")], 
        [InlineKeyboardButton("How to prove your age?", callback_data="How to prove your age?")], 
        [InlineKeyboardButton("Where and When can you drink in Public Places?", callback_data="Where and When can you drink in Public Places?")], 
        [InlineKeyboardButton("Time restrictions for drinking at home", callback_data="Time restrictions for drinking at home")], 
        [InlineKeyboardButton("Can I buy food products containing alcohol after 10.30pm?", callback_data="Can I buy food products containing alcohol after 10.30pm?")], 
        [InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Legal Drinking Age")
        # keyboard2 = telegram.KeyboardButton(text="How to prove your age?")
        # keyboard3 = telegram.KeyboardButton(text="Where and When can you drink in Public Places?")
        # keyboard4 = telegram.KeyboardButton(text="Time restrictions for drinking at home")
        # keyboard5 = telegram.KeyboardButton(text="Can I buy food products containing alcohol after 10.30pm?")
        # keyboard5 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3,keyboard4,keyboard5,keyboard6]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Which Drinking Alcohol category does your case fall under?", reply_markup=reply_markup)

#Legal Drinking Age"
    if text == "Legal Drinking Age":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The legal drinking age in Singapore is 18 years old. Only those aged 18 and above will be able to buy and/or consume alcoholic beverages in licensed premises (such as restaurants and supermarkets) in Singapore. It is illegal for licensed liquor sellers to sell alcoholic beverages to any person below the age of 18 or allow him to consume alcohol in their licensed premises. Sellers who do so may be guilty of an offence under reg 37 of the Customs (Liquors Licensing) Regulations, and be liable on conviction to a fine not exceeding $5,000. However, there is no law penalising persons who drink while underage. Individuals below 18 may also still buy food products containing alcohol, such as alcoholic ice-cream.", reply_markup=reply_markup)

#How to prove your age?
    if text == "How to prove your age?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Singaporean: show NRIC Identification card, Driving licence, or Passport. Foreign: some places may be stricter with the identification mode before allowing you to purchase alcohol or enter clubs.To be safe, you should utilise your Passport or Foreign identification card (Note: Having possession of a fake ID is an offence under section 474 of the Penal Code. A person convicted of forgery can be imprisoned up to 10 years or with fine or both.)", reply_markup=reply_markup)

#Where and When can you drink in Public Places?
    if text == "Where and When can you drink in Public Places?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="A public place is defined as a place which the public may freely access even if such access requires a fee or can be restricted from time to time. These include void decks, road decks and parks but do not include restaurants or pubs. The Liquor (Supply and Consumption) Act prohibits consumption of alcohol in such public places and the sale of alcohol from retail outlets between 10.30pm and 7am. Certain areas including Little India and Geylang Serai are specified as Liquor Control Zones and are restricted even more. Persons that are caught consuming alcohol in these areas will be penalised increasingly by up to 1.5 times. If you are found to be drunk and incapable of taking care of yourself, you may be fined up to $1,000 and/or jailed for up to 1 month. Read our other article for more information on liquor control laws in Singapore.", reply_markup=reply_markup)

#Time restrictions for drinking at home
    if text == "Time restrictions for drinking at home":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Drinking at home is not regulated by the The Liquor (Supply and Consumption) Act. There are no legal restrictions on the timing. You can drink alcohol in the privacy of your own home at any time of the day.", reply_markup=reply_markup)

#Can I buy food products containing alcohol after 10.30pm?
    if text == "Can I buy food products containing alcohol after 10.30pm?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="As of 18 Jan 2019, food products containing more than 0.5% alcohol can be bought after 10.30pm. Such food products may include rum & raisin ice-cream, liquor-infused chocolate and cooking wine. Unlike alcoholic beverages, such food products have been exempted from liquor licensing requirements as they are unlikely to lead to alcohol abuse.", reply_markup=reply_markup)

#Drink Driving
    if text == "Drink Driving":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Drinking Alcohol")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Drinking Alcohol")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="It is a criminal offence to drive while under the influence of alcohol under section 67 of the Road Traffic Act. Specifically, you will be guilty of this offence if you: are unfit to drive under the influence of alcohol to the extent you are incapable of having proper control of the vehicle; or exceed the prescribed alcohol limit. The prescribed alcohol limit is: 35 microgrammes of alcohol in 100 millilitres of breath 80 milligrammes of alcohol in 100 millilitres of blood. If found guilty, you will be liable to fines and may possibly face jail time. Read more about the penalties and sentences for drink-driving in Singapore.", reply_markup=reply_markup)

#Cybercrime
    if text == "Cybercrime":
        kb = [[InlineKeyboardButton("Is It Illegal to Threaten to Beat Someone Up online", callback_data="Is It Illegal to Threaten to Beat Someone Up online")],
        [InlineKeyboardButton("Is it illegal to cheat someone of an in-game item in MMORPGs?", callback_data="Is it illegal to cheat someone of an in-game item in MMORPGs?")],
        [InlineKeyboardButton("What do I do if someone impersonates me online?", callback_data="What do I do if someone impersonates me online?")],
        [InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Is It Illegal to Threaten to Beat Someone Up online")
        # keyboard2 = telegram.KeyboardButton(text="Is it illegal to cheat someone of an in-game item in MMORPGs?")
        # keyboard3 = telegram.KeyboardButton(text="What do I do if someone impersonates me online?")
        # keyboard4 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3,keyboard4]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Which Cybercrime category does your case fall under?", reply_markup=reply_markup)

#Is It Illegal to Threaten to Beat Someone Up online
    if text == "Is It Illegal to Threaten to Beat Someone Up online":

        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Cybercrime")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Cybercrime")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Pursuant to section 503 of the Penal Code, whoever threatens to either inflict injury to another person or damage his property with an intention to cause alarm to the victim, or to compel the victim to do something (or not do something), commits the offence of criminal intimidation. However, it is likely that not all such cases will be prosecuted by the authorities unless there is sufficient concern to do so. Pursuant to section 506 of the Penal Code, criminal intimidation (involving threats of physical violence) is punishable with a jail term of up to 2 years, or a fine, or both.", reply_markup=reply_markup)

#Is it illegal to cheat someone of an in-game item in MMORPGs?
    if text == "Is it illegal to cheat someone of an in-game item in MMORPGs?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Cybercrime")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Cybercrime")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Whether it is illegal to cheat someone of an in-game item in Massively Multiplayer Online Role-Playing Games (MMORPGs) would  depend on the definition of “cheat”. In games such as Team Fortress 2 and World Of Warcraft, players are allowed to trade items. A bargain is not cheating. The CMA lists several offences that are actively prosecuted in Singapore. For example, unauthorised access to computer material (as provided for in section 3 of the CMA) could include hacking into a game account and emptying it of valuable in-game items. The same could be said of exploiting game bugs to steal from other players. Other offences include unauthorised modification of computer material (section 5 of the CMA) and unauthorised password disclosure (section 8 of the CMA).", reply_markup=reply_markup)

#What do I do if someone impersonates me online?
    if text == "What do I do if someone impersonates me online?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Cybercrime")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Cybercrime")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="If you ever come across someone on Facebook or other online services pretending to be you or someone you know, you should first make a report to Facebook or the relevant service provider. (Please do check that it is not a rashly concocted birthday prank beforehand.) After determining that the impersonation is not a prank, you should lodge a police report. The perpetrator may then be charged for cheating by personation under section 416 of the Penal Code, where cheating is defined by section 415 of the Penal Code as an activity which: “fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit to do if he were not so deceived, and which act or omission causes or is likely to cause damage or harm to any person in body, mind, reputation or property” It does not matter whether the person being impersonated is a real or fictitious person. The impersonator may be punishable with an imprisonment up to 5 years, or a fine, or both, as stipulated under section 419 of the Penal Code. Depending on the severity of the communication by the impersonator to the victim, he may also be charged for criminal defamation under section 499 of the Penal Code. Any word or communication, published, written, electronic or media, that lowers the perceived moral or intellectual character of the victim, may render the accused liable for criminal defamation. Civil defamation suits may also be filed if the victim intends to seek compensation.", reply_markup=reply_markup)


#White-Collar Crimes
    if text == "White-Collar Crimes":
        kb = [[InlineKeyboardButton("Insider Trading", callback_data="Insider Trading")],
        [InlineKeyboardButton("Corruption", callback_data="Corruption")],
        [InlineKeyboardButton("Money Laundering", callback_data="Money Laundering")],
        [InlineKeyboardButton("Criminal Breach of Trust", callback_data="Criminal Breach of Trust")],
        [InlineKeyboardButton("Dishonest Assistance and Knowing Receipt", callback_data="Dishonest Assistance and Knowing Receipt")],
        [InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Insider Trading")
        # keyboard2 = telegram.KeyboardButton(text="Corruption")
        # keyboard3 = telegram.KeyboardButton(text="Money Laundering")
        # keyboard4 = telegram.KeyboardButton(text="Criminal Breach of Trust")
        # keyboard5 = telegram.KeyboardButton(text="Dishonest Assistance and Knowing Receipt")
        # keyboard6 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1, keyboard2, keyboard3,keyboard4,keyboard5,keyboard6]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Which White-Collar Crime category does your case fall under?", reply_markup=reply_markup)

#Insider Trading
    if text == "Insider Trading":
        kb = [[InlineKeyboardButton("What is insider trading?", callback_data="What is insider trading?")],
        [InlineKeyboardButton("Criminal and Civil Regime", callback_data="Criminal and Civil Regime")],
        [InlineKeyboardButton("Back", callback_data="White-Collar Crimes")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="What is insider trading?")
        # keyboard2 = telegram.KeyboardButton(text="Criminal and Civil Regime")
        # keyboard2 = telegram.KeyboardButton(text="White-Collar Crimes")
        # custom_keyboard = [[keyboard1, keyboard2,keyboard3]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="You have selected Insider Trading.", reply_markup=reply_markup)


#What is insider trading?
    if text == "What is insider trading?":
        kb = [[InlineKeyboardButton("Punishment", callback_data="Punishment")],
        [InlineKeyboardButton("Back", callback_data="Insider Trading")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Punishment")
        # keyboard2 = telegram.KeyboardButton(text="Insider Trading")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Insider trading is the process of intentionally trading upon proprietary, non-public information concerning a firm’s future by a corporate official or another party in possession of the non-public information. In “traditional” insider trading cases, it involves a company officer like the director, the chief financial officer (CFO) or the company secretary misappropriating non-public information to trade on the company’s shares for their own benefit or to avoid some detriment. In non-traditional cases, it involves a secondary party to the non-public information. Persons like a spouse of the key company officer, a stockbroker who accidentally received non-public information or a waiter who overheard discussion on the company’s non-public information might be found liable for breaching insider trading laws if they acted upon the non-public information.", reply_markup=reply_markup)

#Punishment
    if text == "Punishment":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="What is insider trading?")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="What is insider trading?")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The offence of insider trading is set out under section 218 of the Securities and Futures Act (SFA). For a breach of section 218 of the SFA to be made out, it needs to be established that the person: Is a “person who is connected to a corporation”; Possesses “information concerning that corporation”; The information is not “generally available”; A reasonable person would, if that information were generally available, expect it to have a “material effect on the price or value of securities of that corporation”; The connected person knows or ought reasonably to know that the information is not generally available; and The connected person knows or ought reasonably to know that if the information were generally available, it might have a material effect on the price or value of those securities of that corporation. Once all these limbs are satisfied, a person would be found liable for breaching section 218 of the SFA.", reply_markup=reply_markup)


#Criminal and Civil Regime
    if text == "Criminal and Civil Regime":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Insider Trading")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard1 = telegram.KeyboardButton(text="Insider Trading")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Not all perpetrators of insider trading will be imprisoned. The SFA provides for civil and criminal penalties to punish insider trading. Under section 232(1) of the SFA, the Monetary Authority of Singapore (MAS) can take up a civil penalty action against the wrongdoer with the concurrence of the Public Prosecutor. The court may order the payment of a sum three times of the amount of profit gained or loss avoided as a result of the wrongdoer’s act. If the wrongdoer did not make any profit or suffered any loss as a result of his act, then the court may order the wrongdoer to pay a penalty sum between S$50,000 to S$2 million. Criminal penalties in respect of a breach of section 218 of the SFA is provided for under section 221 of the SFA. A natural person may be fined up to S$250,000 or sentenced to imprisonment for up to 7 years or to both. Section 333 of the SFA provides for a corporation to be fined up to twice the maximum amount prescribed for the relevant offence. When the company is found liable for offences under the SFA, the director, executive officer, secretary or similar officer of the company who knew of the transaction or is a party to the transaction shall also be guilty of the offence. It is also important to note that once a wrongdoer has been penalised under the civil regime, he is not to be punished again under the criminal regime. The standard of proof is also different between the civil and criminal regime in that the Prosecution is required to prove on a balance of probabilities in a civil action in contrast to a prove beyond reasonable doubt for a criminal prosecution.", reply_markup=reply_markup)


#Corruption
    if text == "Corruption":
        kb = [[InlineKeyboardButton("Prevention of Corruption Act and its applications", callback_data="Prevention of Corruption Act and its applications")],
        [InlineKeyboardButton("Punishment for Corruption", callback_data="Punishment for Corruption")],
        [InlineKeyboardButton("Back", callback_data="White-Collar Crimes")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Prevention of Corruption Act and its applications")
        # keyboard2 = telegram.KeyboardButton(text="Punishment for Corruption")
        # keyboard2 = telegram.KeyboardButton(text="White-Collar Crimes")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="You have selected corruption.", reply_markup=reply_markup)

#Prevention of Corruption Act and its applications
    if text == "Prevention of Corruption Act and its applications":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Corruption")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard1 = telegram.KeyboardButton(text="Corruption")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The main offences are listed out in sections 5 and 6 of the PCA. Section 5 of the PCA covers those who corruptly receive and corruptly give gratification as an inducement or reward for a person performing or withholding performance of a transaction while section 6 of the PCA covers the actions of agents, i.e. employees, those who act on behalf of others and public servants. The term “gratification” is also defined broadly and includes monetary rewards, employment, discharge of any loan, service, favour or advantage. To stamp out corruption in the Public Service, the PCA also includes a presumption of corruption under section 8 of the PCA where the gratification is deemed to have been paid or given corruptly as an inducement or reward unless the contrary is proved.", reply_markup=reply_markup)

#Punishment for Corruption
    if text == "Punishment for Corruption":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Corruption")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard1 = telegram.KeyboardButton(text="Corruption")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Under the PCA, the punishment for corruption is a fine not exceeding $100,000 or to a jail term of not exceeding 5 years or to both. However, the maximum jail term is increased from 5 years to 7 years if the transactions involve the Public Service or if the bribery target is a member of parliament or a public servant. Furthermore, if the gratification involves a sum of money or if a value can be attached to the gratification, the court may order the offender to pay a sum equal to the amount of gratification received as a fine. Hence, it is possible for the fine to exceed $100,000 as in the 2017 case involving a Petrochemical Corporation of Singapore marketing and sales executive who was ordered to pay a fine of $1.13 million for corruption. As local SMEs expands regionally and globally for their businesses, it is also important to be cognisant of the extra-territorial effect of the anti-corruption laws in Singapore. Singaporeans who offer bribes or receives bribes overseas will be liable for punishment. SMEs can seek the help of lawyers to advise them on appropriate internal HR practices and business ethics guidelines to ensure that they do not run afoul of Singapore’s corruption laws.", reply_markup=reply_markup)



#Money Laundering
    if text == "Money Laundering":
        
        kb = [[InlineKeyboardButton("What is money laundering?", callback_data="What is money laundering?")],
        [InlineKeyboardButton("Consequences", callback_data="Consequences")],
        [InlineKeyboardButton("Criminal Offence under CDSA (4 main types)", callback_data="Criminal Offence under CDSA (4 main types)")],
        [InlineKeyboardButton("Criminal Offence under Penal Code", callback_data="Criminal Offence under Penal Code")],
        [InlineKeyboardButton("Back", callback_data="White-Collar Crimes")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="What is money laundering?")
        # keyboard2 = telegram.KeyboardButton(text="Consequences")
        # keyboard3 = telegram.KeyboardButton(text="Criminal Offence under CDSA (4 main types)")
        # keyboard4 = telegram.KeyboardButton(text="Criminal Offence under Penal Code")
        # keyboard5 = telegram.KeyboardButton(text="White-Collar Crimes")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3,keyboard4,keyboard5]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="You have selected Money Laundering.", reply_markup=reply_markup)


#What is money laundering?
    if text == "What is money laundering?":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Money Laundering")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Money Laundering")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Money laundering (ML) is defined as a process to make ‘dirty’ money (proceeds from criminal activities) look ‘clean’ (or legitimate) by masking the benefits derived from criminal conduct so that it appears to have originated from a legitimate source.", reply_markup=reply_markup)

#Consequences
    if text == "Consequences":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Money Laundering")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Money Laundering")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The penalty for the commission of the four money laundering offences under section 43, 44, 46 and 47 of the CDSA for an individual is a fine not exceeding $500,000 or a term of imprisonment not exceeding ten years, or both. The penalty for the failure to report cross border movements of cash exceeding prescribed amount under section 48C of the CDSA for an individual is a fine not exceeding $50,000 or a term of imprisonment not exceeding three years, or both. Anyone convicted of sections 411 and 414 of the Penal Code would be punished with a fine or a term of imprisonment which may extend to five years, or both.", reply_markup=reply_markup)

#Criminal Offence under Penal Code
    if text == "Criminal Offence under Penal Code":
        kb = [[InlineKeyboardButton("Dishonestly receiving stolen property", callback_data="Dishonestly receiving stolen property")],
        [InlineKeyboardButton("Disposal and concealment of stolen property", callback_data="Disposal and concealment of stolen property")],
        [InlineKeyboardButton("Back", callback_data="Money Laundering")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Dishonestly receiving stolen property")
        # keyboard2 = telegram.KeyboardButton(text="Disposal and concealment of stolen property")
        # keyboard3 = telegram.KeyboardButton(text="Money Laundering")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Please select the type of Criminal Offence under Penal Code.", reply_markup=reply_markup)

#Disposal and concealment of stolen property
    if text == "Disposal and concealment of stolen property":
        kb = [[InlineKeyboardButton("Back", callback_data="Criminal Offence under Penal Code")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under Penal Code")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Section 414 of the Penal Code criminalises the act of voluntarily assisting in the concealing or disposing of stolen property as long as the person knows or has a reason to believe the property to be stolen.", reply_markup=reply_markup)

#Dishonestly receiving stolen property
    if text == "Dishonestly receiving stolen property":
        kb = [[InlineKeyboardButton("Back", callback_data="Criminal Offence under Penal Code")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under Penal Code")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Section 411 of the Penal Code punishes any person who (a) knows or having reason to believe the property to be stolen property; and (b) dishonestly receives or retains stolen property. The provision may also be used in money laundering cases. In this case, the provision is not limited to any drug dealing offences or serious offences under the relevant schedule in the CDSA. It may be applied in circumstances such as, when a person knew that his friend stole money from the employer (eg. a bank) and kept the stolen money for his friend.", reply_markup=reply_markup)



#Criminal Offence under CDSA (4 main types)
    if text == "Criminal Offence under CDSA (4 main types)":
        kb = [[InlineKeyboardButton("Criminals laundering their own money", callback_data="Criminals laundering their own money")],
        [InlineKeyboardButton("Benefitting from someone else’s money laundering", callback_data="Benefitting from someone else’s money laundering")],
        [InlineKeyboardButton("Abetment of money laundering", callback_data="Abetment of money laundering")],
        [InlineKeyboardButton("Entering into an arrangement to benefit from someone else’s money laundering", callback_data="Entering into an arrangement to benefit from someone else’s money laundering")],
        [InlineKeyboardButton("Back", callback_data="Money Laundering")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Criminals laundering their own money")
        # keyboard2 = telegram.KeyboardButton(text="Benefitting from someone else’s money laundering")
        # keyboard3 = telegram.KeyboardButton(text="Abetment of money laundering")
        # keyboard4 = telegram.KeyboardButton(text="Entering into an arrangement to benefit from someone else’s money laundering")
        # keyboard5 = telegram.KeyboardButton(text="Money Laundering")
        # custom_keyboard = [[keyboard1, keyboard2,keyboard3,keyboard4,keyboard5]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Please select the type of Criminal Offence under CDSA", reply_markup=reply_markup)

#Criminals laundering their own money
    if text == "Criminals laundering their own money":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Criminal Offence under CDSA (4 main types)")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under CDSA (4 main types)")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Offence is committed when a person: (a) conceals or disguises any property which (in whole or in part, directly or indirectly) represents his benefits from drug dealing or from criminal conduct; or (b) converts or transfers that property; or (c) removes it from Singapore. The relevant provisions are sections 46(1) and 47(1) of the CDSA, for benefits from drug dealing and criminal conducts respectively. They apply to criminals who are laundering their own money from drug dealing and other criminal conducts.", reply_markup=reply_markup)

#Benefitting from someone else’s money laundering
    if text == "Benefitting from someone else’s money laundering":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Criminal Offence under CDSA (4 main types)")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under CDSA (4 main types)")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Offence is committed when a person who: (a) knowing or having reasonable grounds to believe that; (b) any property (in whole or in part, directly or indirectly) represents another person’s benefits from drug dealing or criminal conduct; and (c) acquires or has possession of or uses that property. The relevant provisions are sections 46(3) and 47(3) of the CDSA for benefits from drug dealing and criminal conducts respectively. The provisions apply to a third party, who is not a drug dealer or did not commit a criminal conduct himself or herself.", reply_markup=reply_markup)

#Abetment of money laundering 
    if text == "Abetment of money laundering":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Criminal Offence under CDSA (4 main types)")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under CDSA (4 main types)")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Offence is committed when a person who: (a) knowing or having reasonable grounds to believe that; (b) any property (in whole or in part, directly or indirectly) represents, another person’s benefits from drug dealing and criminal conduct; (c) conceals or disguises that property; or (d) converts or transfers that property or removes it from Singapore. The relevant provisions are sections 46(2) and 47(2) of the CDSA. The offence is essentially an offence of abetment (knowingly assisting’), where the third party assists a drug dealer or a person who committed a criminal conduct to make the ‘dirty’ money ‘clean’ again.", reply_markup=reply_markup)

#Entering into an arrangement to benefit from someone else’s money laundering
    if text == "Entering into an arrangement to benefit from someone else’s money laundering":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Criminal Offence under CDSA (4 main types)")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Criminal Offence under CDSA (4 main types)")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Offence is committed when a person who enters into or is otherwise concerned in an arrangement, knowing or having reasonable grounds to believe that, by the arrangement — (a) the retention or control by or on behalf of another (referred to in this section as that other person) of that other person’s benefits of drug dealing or criminal conduct is facilitated (whether by concealment, removal from jurisdiction, transfer to nominees or otherwise); or (b) that other person’s benefits from drug dealing or criminal conduct — (i) are used to secure funds that are placed at that other person’s disposal (directly or indirectly); or (ii) are used for that other person’s benefit to acquire property by way of investment or otherwise, and knowing or having reasonable grounds to believe that that other person is a person who engages in or has engaged in drug dealing or criminal conduct or has benefited from such shall be guilty of an offence. The relevant provisions are sections 43(1) and 44(1) of the CDSA. This offence is also an offence of abetment. This offence criminalises a person assisting a drug trafficker or a serious crime offender to (a) retain or control his benefits from these criminal activities or (b) secure such ‘dirty’ funds or (c) invest such funds. However, the prosecution has to prove that there is an ‘arrangement’ (ie some form of agreement) between the money launderer and the criminal (evidence of such arrangement would typically be some payment of commission) before the offence could be made out.", reply_markup=reply_markup)

#Criminal Breach of Trust
    if text == "Criminal Breach of Trust":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="White-Collar Crimes")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="White-Collar Crimes")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="The definition of Criminal breach of Trust (CBT) in Section 405 of the Penal Code is: When a person is entrusted with property or has dominion over property, and dishonestly misappropriates or converts to his own use that property, he may be liable for the offence of CBT. If he dishonestly uses that property in a way in violation of the law or of any legal contract, he may also be liable for the same offence. Pursuant to section 406 of the Penal Code, the offence of CBT is punishable by imprisonment, fine, or both. Aggravated forms of criminal breach of trust are provided for in sections 407 to 409 of the Penal Code. These include CBT by carriers, clerks or servants, or by public servants, merchants, bankers, or agents respectively. These aggravated forms of CBT attract higher sanctions.", reply_markup=reply_markup)

#Dishonest Assistance and Knowing Receipt
    if text == "Dishonest Assistance and Knowing Receipt":
        kb = [[InlineKeyboardButton("General Definition", callback_data="General Definition")],
        [InlineKeyboardButton("Knowing Receipt", callback_data="Knowing Receipt")],
        [InlineKeyboardButton("Dishonest Assistance", callback_data="Dishonest Assistance")],
        [InlineKeyboardButton("Remedies", callback_data="Remedies")],
        [InlineKeyboardButton("Back", callback_data="White-Collar Crimes")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="General Definition")
        # keyboard2 = telegram.KeyboardButton(text="Knowing Receipt")
        # keyboard3 = telegram.KeyboardButton(text="Dishonest Assistance")
        # keyboard4 = telegram.KeyboardButton(text="Remedies")
        # keyboard5 = telegram.KeyboardButton(text="White-Collar Crimes")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3,keyboard4,keyboard5]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Please select the category from Dishonest Assistance and Knowing Receipt", reply_markup=reply_markup)

#General Definition
    if text == "General Definition":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Dishonest Assistance and Knowing Receipt")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Dishonest Assistance and Knowing Receipt")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="In law, dishonest assistance and knowing receipt are causes of action available to a victim of a breach of trust or a breach of fiduciary relationship against the accessory third party. When do trusts and fiduciary relationships arise A trust arises when a trustee holds the legal title of property on trust for a beneficiary. For instance, lawyers often handle money on their client’s behalf. When the lawyer absconds with the money, this would constitute a breach of trust, amongst other crimes. A fiduciary relationship arises when  has undertaken to act for or on behalf of another in a particular matter in circumstances which give rise to a relationship of trust and confidence. More specifically, in most case the fiduciary has power or discretion; the fiduciary can exercise that power or discretion unilaterally so as to affect the beneficiary’s legal or practical interests; and the beneficiary is particularly vulnerable or dependent upon the fiduciary. Trustees and fiduciaries are not mutually exclusive – a trustee can also be a fiduciary. In the above example, when the lawyer absconds, since he is a fiduciary, he is said to have also committed a breach of fiduciary duty.", reply_markup=reply_markup)

#Knowing Receipt
    if text == "Knowing Receipt":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Dishonest Assistance and Knowing Receipt")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Dishonest Assistance and Knowing Receipt")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Knowing receipt refers to the receiving of assets by a third party who knows that the assets are ill-gotten property originating from a breach of trust or fiduciary duty. Specifically, to sustain an action for knowing receipt, the plaintiff must prove the following matters: the disposal of the plaintiff’s assets in breach of fiduciary duty or trust; the beneficial receipt by the defendant of assets which are traceable as representing the assets of the plaintiff; and knowledge on the part of the defendant that the assets he received are traceable to a breach of fiduciary duty. In an action for knowing receipt, the victim sues the third party who receives the assets in question as a result of the wrongdoing of the primary wrongdoer.", reply_markup=reply_markup)

#Dishonest Assistance
    if text == "Dishonest Assistance":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Dishonest Assistance and Knowing Receipt")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Dishonest Assistance and Knowing Receipt")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Dishonest assistance refers to assistance rendered by a third party to a wrongdoer who breaches a trust or fiduciary relationship. Dishonesty can range from deceitful intention or knowledge, to wilful blindness. A failure to ask questions when suspicious circumstances arise may constitute wilful blindness. Carelessness and stupidity are generally not equated by the courts to dishonesty. Assistance can include anything from actions to omissions – conduct which has made the fiduciary’s breach of duty easier than it would otherwise have been. In an action for dishonest assistance, the victim sues the third party rendering the assistance to the primary wrongdoer.", reply_markup=reply_markup)

#Remedies
    if text == "Remedies":
        kb = [[InlineKeyboardButton("Back to Start", callback_data="Criminal Law")],
        [InlineKeyboardButton("Back", callback_data="Dishonest Assistance and Knowing Receipt")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Dishonest Assistance and Knowing Receipt")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Hence, victims often have no choice but to try to recover their property from the involved third party. For an action of dishonest assistance, the court sometimes allow the victim to recover the value of the misused property or funds, or to order compensation to be paid by the third party. Similarly, for an action of knowing receipt, it may be possible for the victim to recover the misused property or funds from the third party, or seek compensation in lieu.", reply_markup=reply_markup)



#Other Criminal Offences
    if text == "Other Criminal Offences":
        kb = [[InlineKeyboardButton("Suicide", callback_data="Suicide")],
        [InlineKeyboardButton("Feeding Stray Animals", callback_data="Feeding Stray Animals")],
        [InlineKeyboardButton("Back", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Suicide")
        # keyboard2 = telegram.KeyboardButton(text="Feeding Stray Animals")
        # keyboard3 = telegram.KeyboardButton(text="/start")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Please select the category from Other Criminal Offences.", reply_markup=reply_markup)



#Suicide
    if text == "Suicide":
        kb = [[InlineKeyboardButton("Will a Person Who Encourages Another to Commit Suicide be Punished?", callback_data="Will a Person Who Encourages Another to Commit Suicide be Punished?")],
        [InlineKeyboardButton("Attempting suicide", callback_data="Attempting suicide")],
        [InlineKeyboardButton("When Will People Who Commit Suicide be Brought to Court?", callback_data="When Will People Who Commit Suicide be Brought to Court?")],
        [InlineKeyboardButton("Back", callback_data="Other Criminal Offences")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="Will a Person Who Encourages Another to Commit Suicide be Punished?")
        # keyboard2 = telegram.KeyboardButton(text="Attempting suicide")
        # keyboard3 = telegram.KeyboardButton(text="When Will People Who Commit Suicide be Brought to Court?")
        # keyboard4 = telegram.KeyboardButton(text="Other Criminal Offences")
        # custom_keyboard = [[keyboard1,keyboard2,keyboard3,keyboard4]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Select the category that you wish to find out more about.", reply_markup=reply_markup)

#Will a Person Who Encourages Another to Commit Suicide be Punished?
    if text == "Will a Person Who Encourages Another to Commit Suicide be Punished?":
        kb = [[InlineKeyboardButton("Back", callback_data="Suicide")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Suicide")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="a person found guilty of abetting suicide (i.e. aiding another in attempting suicide) will be punished with a fine and also a jail term of up to 10 years, pursuant to section 306 of the Penal Code. This is especially so if such an abettor is motivated by malicious intentions.", reply_markup=reply_markup)

#Attempting suicide
    if text == "Attempting suicide":
        kb = [[InlineKeyboardButton("Back", callback_data="Suicide")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Suicide")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Attempting suicide is illegal in Singapore. It is punishable with a year’s jail, or fine, pursuant to section 309 of the Penal Code. However, it is rarely enforced in reality. This is so as not to aggravate the already delicate emotional well-being of the suicidal person. Therefore, a person who attempts suicide and fails is rarely punished.", reply_markup=reply_markup)

#When Will People Who Commit Suicide be Brought to Court?
    if text == "When Will People Who Commit Suicide be Brought to Court?":
        kb = [[InlineKeyboardButton("Back", callback_data="Suicide")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Suicide")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="This law is usually only enforced against those who repeatedly attempt to commit suicide. This is because the courts have the power to get these people to seek treatment, via a mandatory treatment order.", reply_markup=reply_markup)

#Feeding Stray Animals
    if text == "Feeding Stray Animals":
        kb = [[InlineKeyboardButton("Back", callback_data="Other Criminal Offences")],
        [InlineKeyboardButton("Back to Start", callback_data="Criminal Law")]]
        
        reply_markup = InlineKeyboardMarkup(kb)
        # keyboard1 = telegram.KeyboardButton(text="/start")
        # keyboard2 = telegram.KeyboardButton(text="Suicide")
        # custom_keyboard = [[keyboard1,keyboard2]]
        # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=chat_id, text="Feeding stray animals is not illegal unless littering is involved. If you wish to feed them, do so responsibly, and remember to clean up the mess left behind. However, within Singapore’s National Parks and Nature Reserves, feeding animals, such as monkeys, is an offence prohibited by section 9 of the Parks and Trees Act. ", reply_markup=reply_markup)










def reply(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"].strip()
            chat_id = update["message"]["chat"]["id"]
            username = update["message"]["chat"]["username"]
            
            respond_command(text, chat_id, username)
        except Exception as e:
            print(e)
                        

def send_message(text, chat_id):
    text = urllib.request.pathname2url(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    


def main():
    #last_update_id = None
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(kbCallback))
    updater.start_polling()

    updater.idle()
   # while True:
   #     updates = get_updates(last_update_id)
   #     if len(updates["result"]) > 0:
   #         last_update_id = get_last_update_id(updates) + 1
   #         reply(updates)
   #     time.sleep(0.5)

if __name__ == '__main__':
    main()

def reply(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"].strip()
            chat_id = update["message"]["chat"]["id"]
            username = update["message"]["chat"]["username"]
            
            respond_command(text, chat_id, username)
        except Exception as e:
            print(e)
                        

def send_message(text, chat_id):
    text = urllib.request.pathname2url(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    


def main():
    #last_update_id = None
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(kbCallback))
    updater.start_polling()

    updater.idle()
   # while True:
   #     updates = get_updates(last_update_id)
   #     if len(updates["result"]) > 0:
   #         last_update_id = get_last_update_id(updates) + 1
   #         reply(updates)
   #     time.sleep(0.5)

if __name__ == '__main__':
    main()


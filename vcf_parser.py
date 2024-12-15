#Code Written By: Shawn Chacko (shawn.chacko2008@gmail.com)
#Used For: Removes Duplicate Contacts From iPhone Contact List

import vcf

big_list = []
trash_list = []

reader = open('C:\\Users\\shawn_j8z1ove\\Downloads\\AllContacts_ane.vcf.vcf')


def last_10_digits(num):
    try:
        num = num.strip().replace('-','').replace('(','').replace(')','').replace(' ','')
    
    except Exception as e:
        print(f"{e} for number {num}")
    return num[-10:]


for line in reader:
    if 'BEGIN:VCARD' in line:
        contact_card = dict()
    if line.startswith('N:'):
        x = line.split('N:')
        contact_card['N']= x[-1].strip()
    if line.startswith('FN:'):
        x = line.split('FN:') 
        contact_card['FN'] = x[-1].strip()
    if 'TEL' in line and 'pref' in line:
        x = line.split('pref:')
        contact_card['pref'] = x[-1].strip()
            
    if line.startswith('ORG:'):
        x = line.split('ORG:')
        contact_card['org'] = x[-1].strip()
    if 'END:VCARD' in line:
        in_list = False
        if contact_card.get("pref") is None:
            in_list = True
        else:
            for contact in big_list:
                if contact_card['FN'] == contact['FN'] and contact_card['N'] == contact['N']:
                    in_list = True
                    
                    break
                else:
                    try:
                        cc_last = last_10_digits(contact_card['pref'])
                        c_last = last_10_digits(contact['pref'])
                        #print(f"cc_last: {cc_last}, c_last: {c_last}")
                        if cc_last == c_last:
                            in_list = True
                            break
                        else:
                            pass
                    
                    except Exception as e:
                        print(f"{e} is the error for {contact} <=> {contact_card}")
        if in_list == False:
            big_list.append(contact_card)
        else:
            trash_list.append(contact_card)
                    

print(len(big_list))
print(len(trash_list))
print(len(big_list)+len(trash_list))


out_data = ""

for i in big_list:
    out_data += "BEGIN:VCARD\n"
    out_data += "VERSION:3.0\n"
    out_data += "PRODID:-//Apple Inc.//iPhone OS 16.1.1//EN\n"
    out_data += f"N: {i['N']}\n"
    if "FN" in i:
        out_data += f"FN: {i['FN']}\n"
    if "org" in i:
        out_data += f"ORG:{i['org']}\n"
    if "pref" in i:
        out_data += f"TEL;type=CELL;type=VOICE;type=pref:{i['pref']}\n"
    out_data += "END:VCARD\n"
    
with open("NewContacts_ane.vcf", "w") as fout:
    fout.write(out_data)
    

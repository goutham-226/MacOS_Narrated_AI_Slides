#parse the prompt '1.<vprompt>the prompt</vprompt>/n<vprompt>the prompt</vprompt>


# <vprmpt> 
# 01234567

#str[0]  = <
#str[0+1] = str[1] = v
#str[0+7] = >

#</vprompt> 
#0123456789

#str[0] = <
#str[0+1] = /
#str[0+2] = v
#str[0+9] = >

inpt_string = input('type in your test string')

def parser(str_i):
   Len = len(str_i)
   temp = ""
   for i in range(0,Len):
       if str_i[i] == '<' and str_i[i+1] == 'v' and str_i[i+7] == '>':
            temp = ''
            i = i+7
            continue
       elif str_i[i] == '<' and str_i[i+1] == '/' and str_i[i+2] == 'v' and str_i[i+9] == '>':
              

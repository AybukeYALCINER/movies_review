import glob,os
from webbrowser import open_new_tab
try:
    if not os.path.exists("filmList"):
        os.makedirs("filmList")

    file=open("u.item","r", encoding="utf8")
    file1=open("u.genre","r",encoding="utf-8")
    file2=open("u.user","r",encoding="utf-8")
    file3=open("u.occupation","r",encoding="utf-8")
    file4=open("u.data","r",encoding="utf-8")
    file5=open("review.txt","w",encoding="utf-8")
    general=[i.rstrip('\n') for i in file.readlines()]
    general_split=[i.split("|",4) for i in general]

    release_date=[i[2] for i in general_split]
    imdb_link=[i[3] for i in general_split]
    movie_id=[i[0] for i in general_split]
    movie_title=[i[1] for i in general_split]
    genre_code=[i[-1].split("|") for i in general_split]
    genres_dict={i.rstrip("\n").split("|")[1]:i.rstrip("\n").split("|")[0] for i in file1.readlines()}

    genre_code_english_name=[[genres_dict[str(j)] for j in range(18) if i[j]=="1"]for i in genre_code ]
    user_informations=[i.rstrip("\n").split("|") for i in file2.readlines()]
    occupation_dict={i.rstrip("\n").split("|")[0]:i.rstrip("\n").split("|")[1] for i in file3.readlines()}
    data_information=[i.rstrip("\n").split("\t") for i in file4.readlines()]
    films=[]
    try:
        os.chdir("film")
        for folde in glob.glob("*.txt"):
            FI=open(folde,"r")
            films.append(FI.readlines())

    except (IOError,PermissionError):
        print("there is something which goes wrong about film files")
    finally:
        FI.close()

    class Error(Exception):
        pass
    a=[i[0].split("(") for i in films]
    b=[i[0] for i in a]
    for i in general_split:
        x=i[1].rstrip(i[1][-6:])
        try:
            if i[1]=="unknown":
                file5.write(i[0]+" unknown is not found in folder.Look at 1"+"\n")
            elif x.upper()in b or x.lower() in b or x.title() in b or x in b:
                if "(" in x:
                    z=x.split("(")
                    file5.write(i[0]+" "+z[0].title()+"is found in folder"+"\n")
                else:
                    file5.write(i[0]+" "+x.title()+"is found in folder"+"\n")
            else:
                if "(" in x:
                    z=x.split("(")
                    file5.write(i[0]+" "+z[0].title()+"is not found in folder.Look at "+i[3]+"\n")
                else:
                    file5.write(i[0]+" "+x.title()+"is not found in folder.Look at "+i[3]+"\n")

        except (Error,ValueError):
            file5.write(i[0]+" "+"unknown is not found in folder.Look at 1"+"\n")

    #step üç tamamlanmadı After selecting movies, you will find user ids who rate them from u.data and get detail information about these users from u.user.
    film_item=[]

    for film in films:
        film_general=film[0].split("(")
        film_name=film_general[0]
        film_review=[]
        film_review_str=""
        for indexx in range(len(film[1:])):
            film_review_str+=film[1:][indexx]+ " "
            film_review=[film_review_str]

        for item in general_split:
            movie_name=item[1].rstrip(item[1][-6:])
            if movie_name.upper()==film_name:
               # film_item.append(item+film_review)
                genres=item[4].split("|")

                film_genre_kind=[]
                film_genre_list=""
                for index in range(len(genres)):
                    if genres[index]=="1":
                        film_genre_list+=genres_dict[str(index)]+","
                        #abs.append(genres_dict[str(index)])
                        film_genre_kind=[film_genre_list]
                film_item.append(item+film_review+film_genre_kind)
    ratingData=""
    for i in film_item:
        data_user_id=[]
        data_rating=[]
        user_inf=[]
        for data in data_information:
            if data[1]==i[0]:
                data_user_id.append(data[0])
                data_rating.append(int(data[2]))
                ratingData=data[2]
                for user in user_informations:
                    if data[0]==user[0]:
                        user_inf.append([user[0],user[1],user[2],user[3],user[4]])



        os.chdir('../filmList')
        os.getcwd()
        filename=i[0]+".html"
        file_html=open(filename,"w",encoding="utf-8")

        file_html.write("<html>")
        file_html.write("<head><title>"+i[1].rstrip(i[1][-6:])+"</title></head>")
        file_html.write("<body>")
        file_html.write("<font face='Times New Roman' size='6' color='red'><b>"+i[1].rstrip(i[1][-6:])+"</b></font>")
        file_html.write('<p face="Times New Roman" size="4" color="black"><b>Genre:</b>'+i[-1].rstrip(i[-1][-1])+'</p>')
        file_html.write('<p face="Times New Roman" size="4" color="black"><b>IMDB Link:</b><a href='+i[3]+' target="_self">'+i[1].rstrip(i[1][-6:])+'</a></p>')
        file_html.write('<p face="Times New Roman" size="4" color="black"><b>Review:</b></p>')
        file_html.write('<p face="Times New Roman" size="4" color="black">'+i[5]+'</p>')
        file_html.write('<p face="Times New Roman" size="4" color="black"><b>Total User:</b>'+str(len(data_user_id))+'<b>/Total Rate:</b>'+str(sum(data_rating)/len(data_rating))+'</p>')
        file_html.write("<p></p>")
        file_html.write('<p face="Times New Roman" size="4" color="black"><b>User who rate the film: </b></p>')
        for i in range(len(data_user_id)):
             file_html.write('<p face="Times New Roman" size="4" color="black"><b>User:</b>'+user_inf[i][0]+'<b> Rate:</b>'+str(data_rating[i])+'</p>')
             file_html.write('<p face="Times New Roman" size="4" color="black"><b>User Detail:</b><b> Age:</b>'+user_inf[i][1]+'<b> Gender:</b>'+user_inf[i][2]+'<b> Occupation:</b>'+occupation_dict[user_inf[i][3]]+'<b> Zip Code</b>'+user_inf[i][4]+'</p>')

        file_html.write('</body>')
        file_html.write('</html>')
        file_html.close()

    os.chdir('../')
    os.getcwd()
    file6=open("stopwords.txt","r",encoding="utf-8")
    stepwords=[]
    for i in file6.readlines():
        i=i.rstrip("\n")
        stepwords.append(i)
    word_equal=[]
    words=""
    for item in film_item:
        for word in stepwords:
            if word in item[5]:
                words+=word+","
        word_equal.append([[item[-1].rstrip(item[-1][-1])],words])

    os.chdir("filmGuess")
    final=[]
    for file_name in glob.glob("*.txt"):
        FA=open(file_name,"r",encoding="utf-8")
        final_bir=set()
        final_sifir=FA.readline()
        for i in FA.readlines():
            i=i.split()
            for x in i:
                final_bir.add(x)
        final.append([final_sifir,final_bir])

    FA.close()
    os.chdir("../")
    file7=open("filmGenre.txt","w",encoding="utf-8")
    equal_word=[]
    for i in film_item:
        A=set()
        for z in i[5:-1]:
            x=z.split()
            for word in x:
                if word[-1]==",":
                    word=word.rstrip(",")
                for stop in stepwords:
                    if stop==word:
                        word=word.rstrip(word)
                A.add(word)
        equal_word.append([i[-1].rstrip(i[-1][-1]),A])

    equal_word_second=[]

    unknown=set()
    Action=set()
    Adventure=set()
    Animation=set()
    Children_s=set()
    Comedy=set()
    Crime=set()
    Documentary=set()
    Drama=set()
    Fantasy=set()
    Film_Noir=set()
    Horror=set()
    Musical=set()
    Mystery=set()
    Romance=set()
    Sci_Fi=set()
    Thriller=set()
    War=set()
    Western=set()
    for lists in equal_word:
        for kind in lists[0].split(","):
            for words in lists[1]:
                if "unknown" == kind:
                    unknown.add(words)
                elif "Action" == kind:
                    Action.add(words)
                elif "Adventure" == kind:
                    Adventure.add(words)
                elif "Animation" == kind:
                    Animation.add(words)
                elif "Children's" == kind:
                    Children_s.add(words)
                elif "Comedy" == kind:
                    Comedy.add(words)
                elif "Crime" == kind:
                    Crime.add(words)
                elif "Documentary" == kind:
                    Documentary.add(words)
                elif "Drama" == kind:
                    Drama.add(words)
                elif "Fantasy" == kind:
                    Fantasy.add(words)
                elif "Film-Noir" == kind:
                    Film_Noir.add(words)
                elif "Horror" == kind:
                    Horror.add(words)
                elif "Musical" == kind:
                    Musical.add(words)
                elif "Mystery"==kind:
                    Mystery.add(words)
                elif "Romance" == kind:
                    Romance.add(words)
                elif "Sci-Fi" == kind:
                    Sci_Fi.add(words)
                elif "Thriller" == kind:
                    Thriller.add(words)
                elif "War" == kind:
                    War.add(words)
                elif "Western"==  kind:
                    Western.add(words)

    catogory=[["unknown",unknown],["Action",Action],["Adventure",Adventure],["Animation",Animation],["Children's",Children_s],["Comedy",Comedy],["Crime",Crime],["Documentary",Documentary],["Drama",Drama],["Fantasy",Fantasy],["Film-Noir",Film_Noir],["Horror",Horror],["Musical",Musical],["Mystery",Mystery],["Romance",Romance],["Sci-Fi",Sci_Fi],["Thriller",Thriller],["War",War],["Western",Western]]
    lisye=[]

    for i in final:
        for cat in catogory:
            count=0
            for each in cat[1]:
                if each in i[1] and each!='' and each!="":
                    count+=1
            if int(count)-4>=20:
                lisye.append([i[0].split("(")[0],catogory[catogory.index(cat)][0],int(count)])




    file7.write("Guess Genres of Movie based on Movies"+"\n")
    for elmet in range(len(final)):
        a=set()
        name=final[elmet][0].split("(")[0]
        file7.write(name+":")
        for i in lisye:
            kinds=""
            if name==i[0]:
                a.add(i[1]+" ")
        for x in a:
            kinds+=x
        file7.write(kinds)
        file7.write("\n")

except IOError:
    print("There are some mistekes about files")
finally:
    file.close()
    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()
    file6.close()
    file7.close()


#Luke McEvoy

#Pledge: I have pledged my honor that I have abided by the Stevens Honor System.

PREF_FILE = 'musicrecplus.txt'

def main():
    dictionary = load_users(PREF_FILE)
    username = input('Enter your name (put a $ symbol after your name if you wish your preferences to remain private):')
    if username not in dictionary:
        get_preferences(username, dictionary, PREF_FILE)
    menu(username, dictionary)
    
def load_users(fileName):
    ''' Loads users and preferences from file, if file does not exist writes to new file.'''
    dict = {}
    try:
        file = open(fileName, 'r')
    except:
        file = open(fileName, 'w')
        file.close()
        return dict
    for line in file:
        if line == '\n':
            pass
        else:
            user, artists = line.split(':')
            artists = artists.split(',')
            dict[user] = []
            for x in artists:
                if x[-1] == '\n':
                    x = x[:-1]
                dict[user].append(x)
    file.close()
    return dict

def get_preferences(user, dict, filename):
    ''' Gets user's preferences. '''
    artists = []
    #if user in dict:
    new_pref = input('Enter an artist that you like (Enter to finish):')
    while new_pref != '':
        artists.append(new_pref)
        new_pref = input('Enter an artist that you like (Enter to finish):')
    artists.sort()
    save(user, dict, filename, artists)
    return artists

def save(user, dict, filename, prefs):
    ''' Saves preferences to the file. '''
    dict[user] = prefs
    file = open(filename, 'w')
    new_lines = []
    for user in dict:
        new_lines.append(str(user)+':' + ','.join(dict[user]) + '\n')
    new_lines.sort()
    for x in new_lines:
        file.write(x)
    file.close()
    
def menu(user, dict):
    while True:
        print('Enter a letter to choose an option:\ne - Enter preferences\nr - Get recommendations\np - Show most popular artists\nh - How popular is the most popular\nm - Which user has the most likes\nq - Save and quit')
        choice = input()
        if choice is 'e':
            get_preferences(user, dict, PREF_FILE)
        elif choice is 'r':
            prefs = dict[user]
            recs = get_recommendations(dict, user, prefs)
            print_recs(recs, user)
            save(user, dict, PREF_FILE, prefs)
        elif choice is 'p':
            best = pop_artist(dict, 'people')
            print_pop_artists(best)
        elif choice is 'h':
            how_popular(dict)
        elif choice is 'm':
            most_likes(dict)
        elif choice is 'q':
            try:
                save(user, dict, PREF_FILE, dict[user])
                break
            except:
                break
            
def get_recommendations(dict, user, prefs):
    '''Returns the artist preferences of the person with the most matched artists with the user.'''
    best_users = []
    best_score = 0
    for name in dict:
        if name[-1] == '$':
            continue
        if dict[user] != dict[name]:
            currentprefs = dict[user]
            mainprefs = dict[name]
            matches = 0
            currentprefs.sort()
            mainprefs.sort()
            i = 0
            j = 0
            while i < len(currentprefs) and j < len(mainprefs):
                if currentprefs[i] == mainprefs[j]:
                    matches += 1
                    i += 1
                    j += 1
                elif currentprefs[i] < mainprefs[j]:
                    i += 1
                else:
                    j += 1
            if matches > best_score:
                best_score = matches
                best_users = [name]
            if matches == best_score:
                best_users.append(name)
    list_of_recs = []
    
    def drop_matches(A, B):
        '''Returns list of elements that contains only the elements in B that are not in A.'''
        A.sort()
        B.sort()
        not_matches = []
        i = j = 0
        while i < len(A) and j < len(B):
            if A[i] == B[j]:
                j += 1
            elif A[i] > B[j]:
                not_matches.append(B[j])
                j += 1
            else:
                i += 1
        while j < len(B):
            not_matches.append(B[j])
            j+=1
        return not_matches
    
    def drop_duplicates(A):
        A.sort()
        if A == []:
            not_duplicates = []
            return not_duplicates
        not_duplicates = [A[0]]
        i = 0
        j = 1
        while i < len(A):
            if i+j == len(A):
                break
            if A[i] == A[i+j]:
                j += 1
            else:
                not_duplicates.append(A[i+j])
                i += j
                j = 1
        return not_duplicates
    
    for x in best_users:
        for y in dict[x]:
            if y == '':
                break
            if y[-1] == '\n':
                list_of_recs.append(y[:-1])
            else:
                list_of_recs.append(y)
    return drop_duplicates(drop_matches(dict[user], list_of_recs))

def print_recs(recs, user):
    '''Prints out the user's list of recommended artists.'''
    if recs == []:
        print('No recommendations available at this time')
    else:
        print('\n'.join(recs))

def pop_artist(dict, func):
    '''Finds the most popular artist out of the ones listed in the dictionary.'''
    pop_artists = {}
    max_val = 0
    most_popular = []
    for user in dict:
        if user[-1] == '$':
            continue
        for x in dict[user]:
            if x[-1] == '\n':
                x = x[:-1]
            if x in pop_artists:
                pop_artists[x] += 1
            else:
                pop_artists[x] = 1
            if pop_artists[x] > max_val:
                    max_val = pop_artists[x]
                    most_popular = [x]
            elif pop_artists[x] == max_val:
                most_popular.append(x)
    
    if func == 'people':
        return most_popular
    elif func == 'num':
        return max_val

def print_pop_artists(best):
    '''Prints the list of most popular artists.'''
    if best == []:
        print('Sorry, no artists found')
    if len(best) == 1:
        print(best[0])
    else:
        print('\n'.join(best))

def how_popular(dict):
    '''Calculates how popular the most popular artist(s) is.'''
    best_val = pop_artist(dict, 'num')
    if best_val == 0:
        print('Sorry, no artists found')
    else:
        print(str(best_val))
        
def most_likes(dict):
    '''Print the full name(s) of the user(s) who likes the most artists.'''
    most_like_users = []
    max_likes = 0
    for user in dict:
        if user[-1] == '$':
            continue
        if len(dict[user]) > max_likes:
            most_like_users = [user]
            max_likes = len(dict[user])
        elif len(dict[user]) == max_likes:
            most_like_users.append(user)
    if most_like_users == []:
        print('Sorry, no user found')
    elif len(most_like_users) == 1:
        print(most_like_users[0])
    else:
        print('\n'.join(most_like_users))
        
main()

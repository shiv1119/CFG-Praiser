from django.shortcuts import render
from django.http import HttpResponse

def to_string(n):
    return str(n)

def bfs(state, path, rules):
    if len(state) == 1:
        result = "YES\n" + ' '.join(path)
        return True, result

    for idx, (non_terminal, rule) in enumerate(rules):
        location = state.find(rule)
        
        if location != -1:
            new_state = state[:location] + non_terminal + state[location + len(rule):]
            new_path = path + [str(idx + 1)] 
            found, output = bfs(new_state, new_path, rules)
            if found:
                return True, output 
    
    return False, "NO" 


def check_grammar(request):
    if request.method == "POST":
        terminals = request.POST.get('terminals', '')
        non_terminals = request.POST.get('non_terminals', '')
        rules_input = request.POST.get('rules', '').splitlines()
        words_input = request.POST.get('words', '').splitlines()

        rules = []
        for rule in rules_input:
            parts = rule.split('->')
            if len(parts) == 2:
                non_terminal = parts[0].strip()
                production = parts[1].strip()
                rules.append((non_terminal, production))

        results = []
        for word in words_input:
            found, output = bfs(word, [], rules)
            results.append(output)
        
        return render(request, 'cfgpraserapp/home.html', {'results': results})

    return render(request, 'cfgpraserapp/home.html')

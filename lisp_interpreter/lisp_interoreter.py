def tokenize(text:str)->list :
    text=text.replace("("," ( ")
    text=text.replace(")"," ) ")
    list_text=text.split()
    return list_text

def atom(token:str):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token
        
def read_from_tokens(tokens:list):
    if len(tokens)==0 :
        raise SyntaxError("unexpected EOF")
    token=tokens.pop(0)

    if token=="(" :
        L=[]
        while tokens[0]!=")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token==")" :
        raise SyntaxError("unexpected )")
    else:
        return atom(token)
    
global_env={
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    'pow': lambda a, b: a**b,
    ">":lambda a,b:a>b,
    "<":lambda a,b:a<b,
    "=":lambda a,b:a==b,
    "head": lambda lst : lst[0],
    "rest": lambda lst : lst[1:],
    "concat": lambda head,lst : [head,*lst],
}


def evaluate(x,env=global_env):
    if isinstance(x,str):
        return env[x]
    elif not isinstance(x,list):
        return x

    elif x[0]=="define":
        var_name=x[1]
        var_vlaue=x[2]

        env[var_name]=evaluate(var_vlaue,env)

    #if else 判断
    elif x[0]=="if":
        condition=x[1]
        true_condition=x[2]
        false_condition=x[3]
        return evaluate(true_condition,env) if evaluate(condition,env)  else evaluate(false_condition,env) 
    #自定义函数
    elif x[0]=="lambda":
        param=x[1]
        body=x[2]

        def proc(*args):
            local_env=env.copy()

            for x,y in zip(param,args) :
                local_env[x]=y

            return evaluate(body,local_env)
        return proc
    elif x[0]=="quote":
        return x[1]
    
    elif x[0]=="begin":
        l=[]
        for i in x[1:]:
            l.append(evaluate(i,env))
        return l[-1]
    else:
        func=evaluate(x[0],env)
        args=[evaluate(arg,env) for arg in x[1:]]

        return func(*args)
    

def repl():
    print("欢迎来到微型 Lisp 控制台！(输入 'quit' 退出)")
    while True:
        try:
            user_input = input("lisp> ")
            if user_input.strip() == 'quit':
                break
            
            # 读取 (Read)
            tokens = tokenize(user_input)
            ast = read_from_tokens(tokens)
            
            # 3. 求值 (Eval)
            result =evaluate(ast)
            
            
            print(result)
            
        except Exception as e:
            # 如果代码有错（比如少了个括号），打印错误而不是崩溃
            print(f"错误: {e}")

repl()
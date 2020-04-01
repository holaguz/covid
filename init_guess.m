function ypred = init_guess(p, t)
    beta = p(1); gamma = p(2);
    I_0 = p(3); N = p(4);
    init_cond = I_0;
    
    f = @(a,t) a(1)*(beta*N - gamma);
    [~, ypred] = ode45(f,t,init_cond);
end
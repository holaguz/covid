function ypred = covid(p, t)
    beta_0 = p(1); gamma = p(2);
    S_0 = p(3); I_0 = p(4); R_0 = p(5); N = p(6);
    init_cond = [S_0 I_0 R_0 beta_0];

    f = @(t,a) [-a(3)*a(2)*a(1)/N; 
                a(3)*a(2)*a(1)/N - gamma*a(2);
                gamma*a(2);
                beta_0];
    [~, ypred] = ode45(f,t,init_cond);
end
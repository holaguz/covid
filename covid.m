function ypred = covid(p, t)
    beta = p(1); gamma = p(2);
    S_0 = p(3); I_0 = p(4); R_0 = p(5); N = p(6);
    init_cond = [S_0 I_0 R_0];
    f = @(t,a) [-beta*a(1)*a(2)/N; %ds/dt = -b*s*i
                beta*a(2)*a(1)/N - gamma*a(2); %di/dt = b*s*i - g*i
                gamma*a(2)]; %dr/dt = g*i
            
            
    %f = @(t,a) [-beta*a(1)*a(2)/N; %ds/dt = -b*s*i
    %            beta*a(2)*a(1)/N - gamma*a(2); %di/dt = b*s*i - g*i
    %            gamma*a(2)]; %dr/dt = g*i
            
            
    [~, ypred] = ode45(f,t,init_cond);
    %ypred
end
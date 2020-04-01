function fit_data(S, I, R, t_start, t_end)

t = t_start:t_end; t = t';

S_01 = S(1); I_01 = I(1); R_01 = R(1);
S_0 = S(t_start); I_0 = I(t_start); R_0 = R(t_start);

S = S(t_start:t_end);
I = I(t_start:t_end);
R = R(t_start:t_end);
N = S(1);


beta_init = 0.17; gamma_init = 0.083;

lower_bounds = [0 0 S_0 I_0 R_0 N];
%lower_bounds = [0 0];
upper_bounds = [10 10 S_0 I_0 R_0 N];
%upper_bounds = [];

init_cond = [beta_init gamma_init S_0 I_0 R_0 N];
%init_cond = [beta_init gamma_init S_0 1 1 N];

%t
%[S I R]

options = optimoptions('lsqcurvefit','Algorithm','trust-region-reflective', 'MaxIterations', 10E3, 'Display', 'iter', 'MaxFunctionEvaluations', 10E3);
[pfit, res] = lsqcurvefit(@covid, init_cond, t, [S I R], lower_bounds, upper_bounds, options);
%[pfit, res] = lsqcurvefit(@covid, init_cond, t, [S I R], [], [], options);

beta_hat = pfit(1); gamma_hat = pfit(2);
[beta_hat gamma_hat]
res



t_big = (t_start:8*t_end)'; 
t_smol = (1:1.2*t_end)';

fittedfunc = covid([beta_hat gamma_hat S_0 I_0 R_0 N], t_big);

close all;
figure(1);
subplot(2,3,1)

hold on;
plot(t_smol, fittedfunc(1+t_smol,1));
scatter(t, S, '.r');
legend('Susceptible')
hold off;

subplot(2,3,2)
hold on;
plot(t_smol, fittedfunc(1+t_smol,2));
scatter(t, I, '.r');
legend('Infected')
hold off;

subplot(2,3,3)
hold on;
plot(t_smol, fittedfunc(1+t_smol,3));
scatter(t, R, '.r');
legend('Recovered')
hold off;

subplot(2,3,[4 5 6])
plot(t_big, fittedfunc())
%legend(['Susceptible', 'Infected', 'Recovered'])
end
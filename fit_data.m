function fit_data(S, I, R, N)

t = 0:length(S) - 1; t = t';
%t = 1:length(S); t = t';

S_0 = S(1); I_0 = I(1); R_0 = R(1);
beta_init = -1; gamma_init = 0;

lower_bounds = [0 0 S_0 I_0 R_0 N];
upper_bounds = [5 5 S_0 I_0 R_0 N];

init_cond = [beta_init gamma_init S_0 I_0 R_0 N];
options = optimoptions('lsqcurvefit','Algorithm','trust-region-reflective', 'MaxIterations', 10E3, 'Display', 'iter', 'MaxFunctionEvaluations', 10E3);
[pfit, res] = lsqcurvefit(@covid, init_cond, t, [S I R], lower_bounds, upper_bounds, options);
%[pfit, res] = lsqcurvefit(@covid, init_cond, t, [S I R], [], [], options);

beta_hat = pfit(1); gamma_hat = pfit(2);
[beta_hat gamma_hat]
res



t_est = 1:8*length(t); t_est = t_est';
fittedfunc = covid([beta_hat gamma_hat S(1) I(1) R(1) N], t_est);

close all;
figure(1);
subplot(2,3,1)

hold on;
plot(t, fittedfunc(1+t,1));
scatter(t, S, '.r');
legend('Susceptible')
hold off;

subplot(2,3,2)
hold on;
plot(t, fittedfunc(1+t,2));
scatter(t, I, '.r');
legend('Infected')
hold off;

subplot(2,3,3)
hold on;
plot(t, fittedfunc(1+t,3));
scatter(t, R, '.r');
legend('Recovered')
hold off;

subplot(2,3,[4 5 6])
plot(t_est, fittedfunc())
end
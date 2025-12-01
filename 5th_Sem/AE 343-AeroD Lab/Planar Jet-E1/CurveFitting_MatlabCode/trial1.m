clearvars

load v_val.txt;
load y_val.txt;

f = fit(y_val, v_val, 'gauss1');
disp(['The centerline velocity is ',num2str(f.a1), ...
	', the half-width is ',num2str(f.c1*sqrt(log(2))), ...
	', and the centerline is at y = ',num2str(f.b1)])

y = 128.2:0.1:136;
u = f(y);

fh = figure('Name','Gaussian curve fitting');
plot(u,y,'LineWidth',0.2,'Color','k');
hold on;
plot(v_val,y_val,'Marker','o',...
                 'LineStyle','none',...
                 'MarkerSize',5.0,...
                 'MarkerFaceColor','k',...
                 'MarkerEdgeColor','none');
hold off; grid off; box on;
set(gcf,'Color','w'); set(gca,'Color','w');
set(gca,'FontName','Garamond','FontSize',14);
set(gcf,'Units','Centimeters');
set(gcf,'Position', [ 10 7 24 8 ]);
xlabel('$U$, $ms^{-1}$','Interpreter','Latex');
ylabel('$y$, $cm$','Interpreter','Latex');
legend('Gaussian fit','Measured data');
set(legend,'Location','Best');
set(legend,'Orientation','Horizontal');
set(legend,'Box','Off');
import matplotlib.pyplot as plt
def ExportMapForamt(FormatType, infoMap, modaliity, path, figure):

    PatientName = infoMap.MRI[0][0].PatientName.family_name[:4]

    if FormatType == 'PNG':
        for i in range(len(infoMap.infomap)):
            # fig, ax = plt.subplots()  # Cria uma nova figura e eixo
            # im = ax.imshow(infoMap.infomap[i][0], cmap='hot', aspect='auto', clim=(infoMap.Boundaries[i]))
            # cbar = plt.colorbar(im)  # Adiciona colorbar
            #
            # # Configuração da colorbar e texto em branco
            # cbar.ax.yaxis.set_tick_params(color='white')
            # cbar.set_label('Relaxation Time (ms)', color='white')
            # cbar.ax.tick_params(axis='y', which='both', length=0)
            # cbar.ax.yaxis.set_major_locator(plt.MultipleLocator(base=10))
            # for t in cbar.ax.get_yticklabels():
            #     t.set_color('white')
            #
            # # Configuração das etiquetas de eixo em branco
            # ax.set_xticks([])
            # ax.set_yticks([])
            # ax.axis('off')
            #
            # # Salva a figura
            # plt.savefig(path + '/' + PatientName + "_" + modaliity + "_" + str(infoMap.infomap[i][3])[:5] + '.png',bbox_inches='tight', transparent=True)
            # plt.close()


            figure.savefig(path + '/' + PatientName + "_" + modaliity + "_" + str(infoMap.infomap[i][3])[:5] + '.png',bbox_inches='tight', transparent=True)
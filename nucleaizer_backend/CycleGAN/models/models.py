def create_model(opt):
    model = None
    print(opt.model)
    if opt.model == 'cycle_gan':
        assert(opt.dataset_mode == 'unaligned')
        from . import cycle_gan_model
        model = cycle_gan_model.CycleGANModel()
    elif opt.model == 'pix2pix':
        assert(opt.dataset_mode == 'aligned')
        from . pix2pix_model import Pix2PixModel
        model = Pix2PixModel()
    elif opt.model == 'test':
        assert(opt.dataset_mode == 'single')
        from . import test_model
        model = test_model.TestModel()
    else:
        raise ValueError("Model [%s] not recognized." % opt.model)
    model.initialize(opt)
    print("model [%s] was created" % (model.name()))
    return model

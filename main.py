import controller.CommentsController

if __name__ == '__main__':
    root = controller.CommentsController.CommentsController().get_view()
    # root.update_main_window_layout_min_size()
    root.main_loop()
